# SmartPump — Main Flask application (routes, API calls, database logic)

import os
import csv
import io
import requests
import resend
import mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# App setup
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "smartpump-dev-key")
resend.api_key = os.getenv("RESEND_API_KEY")


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


@app.route("/health")
def health():
    return "ok", 200


@app.route("/")
def home():
    return redirect(url_for("cheapest"))


@app.route("/cheapest", methods=["GET", "POST"])
def cheapest():
    stations = []
    search_term = ""
    fuel_type = "1"
    payment_method = "cash_or_credit"
    fuel_names = {"1": "Regular", "2": "Midgrade", "3": "Premium", "4": "Diesel"}

    if request.method == "POST":
        search_term = request.form.get("search", "")
        fuel_type = request.form.get("fuel_type", "1")
        payment_method = request.form.get("payment_method", "cash_or_credit")

        api_url = "https://api.apify.com/v2/acts/johnvc~fuelprices/run-sync-get-dataset-items"
        response = requests.post(
            api_url,
            params={"token": os.getenv("APIFY_API_TOKEN")},
            json={"search": search_term, "fuel": int(fuel_type)},
            timeout=30
        )

        if response.status_code == 201:
            raw_stations = response.json()

            for station in raw_stations:
                price_cash = station.get("price_cash") or 0
                price_credit = station.get("price_credit") or 0

                if payment_method == "credit_only":
                    display_price = price_credit if price_credit > 0 else None
                    price_label = "CREDIT"
                else:
                    if price_cash > 0 and price_credit > 0:
                        if price_cash <= price_credit:
                            display_price = price_cash
                            price_label = "CASH"
                        else:
                            display_price = price_credit
                            price_label = "CREDIT"
                    elif price_cash > 0:
                        display_price = price_cash
                        price_label = "CASH"
                    elif price_credit > 0:
                        display_price = price_credit
                        price_label = "CREDIT"
                    else:
                        display_price = None
                        price_label = "N/A"

                stations.append({
                    "id": station.get("id"),
                    "name": station.get("name", "Unknown"),
                    "address": station.get("address_line1", ""),
                    "city": station.get("address_locality", ""),
                    "region": station.get("address_region", ""),
                    "zip_code": station.get("address_postalCode", ""),
                    "rating": station.get("starRating"),
                    "display_price": display_price,
                    "price_label": price_label,
                    "price_cash": price_cash,
                    "price_credit": price_credit,
                })

            priced = [s for s in stations if s["display_price"] is not None]
            unpriced = [s for s in stations if s["display_price"] is None]
            priced.sort(key=lambda s: s["display_price"])
            stations = priced + unpriced

    return render_template(
        "cheapest.html",
        stations=stations,
        search_term=search_term,
        fuel_type=fuel_type,
        fuel_name=fuel_names.get(fuel_type, "Regular"),
        payment_method=payment_method
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.")
            return redirect(url_for("signup"))

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("signup"))

        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id FROM Users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            flash("An account with that email already exists.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        cursor.execute(
            "INSERT INTO Users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        user_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO UserReportSettings (user_id, weekly_report_enabled) VALUES (%s, %s)",
            (user_id, False)
        )

        connection.commit()
        cursor.close()
        connection.close()

        flash("Account created! Please log in.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("All fields are required.")
            return redirect(url_for("login"))

        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if not user:
            flash("No account found with that email.")
            return redirect(url_for("login"))

        if not check_password_hash(user["password_hash"], password):
            flash("Incorrect password.")
            return redirect(url_for("login"))

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        return redirect(url_for("cheapest"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("cheapest"))


@app.route("/fillup", methods=["GET", "POST"])
def fillup():
    if not session.get("user_id"):
        flash("Please log in to log a fill-up.")
        return redirect(url_for("login"))

    if request.method == "POST":
        api_station_id = request.form.get("station_id", "")
        station_name = request.form.get("name", "")
        address = request.form.get("address", "")
        city = request.form.get("city", "")
        region = request.form.get("region", "")
        zip_code = request.form.get("zip_code", "")
        rating = request.form.get("rating", "")
        fuel_type_id = int(request.form.get("fuel_type", "1"))
        payment_type = request.form.get("payment_type", "")
        price_per_gallon = float(request.form.get("price_per_gallon", "0"))
        gallons = float(request.form.get("gallons", "0"))
        total_cost = round(price_per_gallon * gallons, 2)

        if not payment_type or gallons <= 0 or price_per_gallon <= 0:
            flash("Please fill in all fields.")
            return redirect(request.url)

        rating_value = None
        if rating and rating != "None":
            try:
                rating_value = float(rating)
            except ValueError:
                rating_value = None

        connection = get_db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id FROM GasStations WHERE api_station_id = %s", (api_station_id,))
        existing_station = cursor.fetchone()

        if existing_station:
            station_db_id = existing_station["id"]
        else:
            cursor.execute(
                "INSERT INTO GasStations (api_station_id, name, address, city, region, zip_code, rating) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (api_station_id, station_name, address, city, region, zip_code, rating_value)
            )
            station_db_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO FillUps (user_id, station_id, fuel_type_id, payment_type, gallons, price_per_gallon, total_cost) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (session["user_id"], station_db_id, fuel_type_id, payment_type, gallons, price_per_gallon, total_cost)
        )

        connection.commit()
        cursor.close()
        connection.close()

        flash("Fill-up logged successfully!")
        return redirect(url_for("cheapest"))

    return render_template("fillup.html")


@app.route("/reports", methods=["GET", "POST"])
def reports():
    if not session.get("user_id"):
        flash("Please log in to view reports.")
        return redirect(url_for("login"))

    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT weekly_report_enabled FROM UserReportSettings WHERE user_id = %s",
        (session["user_id"],)
    )
    settings = cursor.fetchone()
    weekly_enabled = settings["weekly_report_enabled"] if settings else False
    cursor.close()
    connection.close()

    if request.method == "POST":
        report_type = request.form.get("report_type")

        if report_type == "this_week":
            today = datetime.utcnow()
            monday = today - timedelta(days=today.weekday())
            start_date = monday.strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")
        elif report_type == "custom_range":
            start_date = request.form.get("start_date", "")
            end_date = request.form.get("end_date", "")
            if not start_date or not end_date:
                flash("Please select both start and end dates.")
                return redirect(url_for("reports"))
        else:
            flash("Invalid report type.")
            return redirect(url_for("reports"))

        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.fill_date, g.name AS station, g.address, ft.name AS fuel_type,
                   f.payment_type, f.gallons, f.price_per_gallon, f.total_cost
            FROM FillUps f
            JOIN GasStations g ON f.station_id = g.id
            JOIN FuelTypes ft ON f.fuel_type_id = ft.id
            WHERE f.user_id = %s AND DATE(f.fill_date) BETWEEN %s AND %s
            ORDER BY f.fill_date
        """, (session["user_id"], start_date, end_date))
        fillups = cursor.fetchall()
        cursor.close()
        connection.close()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Station", "Address", "Fuel Type", "Payment Type", "Gallons", "Price/Gal", "Total"])

        for f in fillups:
            est_date = f["fill_date"] - timedelta(hours=4)
            writer.writerow([
                est_date.strftime("%Y-%m-%d"),
                f["station"],
                f["address"],
                f["fuel_type"],
                f["payment_type"],
                f["gallons"],
                f["price_per_gallon"],
                f["total_cost"]
            ])

        csv_content = output.getvalue()
        output.close()

        user_email = session.get("user_email", "")
        filename = f"smartpump_report_{start_date}_to_{end_date}.csv"

        try:
            resend.Emails.send({
                "from": "SmartPump <onboarding@resend.dev>",
                "to": [user_email],
                "subject": f"SmartPump — Your Gas Spending Report ({start_date} to {end_date})",
                "html": f"<p>Hi {session.get('user_name', '')}!</p><p>Here's your fill-up report for {start_date} to {end_date}.</p><p>— SmartPump</p>",
                "attachments": [{"filename": filename, "content": list(csv_content.encode("utf-8"))}]
            })
            flash("Report sent to your email!")
        except Exception as e:
            flash(f"Failed to send report: {str(e)}")

        return redirect(url_for("reports"))

    return render_template("reports.html", weekly_enabled=weekly_enabled)


@app.route("/toggle-weekly-report", methods=["POST"])
def toggle_weekly_report():
    if not session.get("user_id"):
        return jsonify({"success": False}), 401

    data = request.get_json()
    enabled = data.get("enabled", False)

    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE UserReportSettings SET weekly_report_enabled = %s WHERE user_id = %s",
        (enabled, session["user_id"])
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
