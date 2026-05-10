# SmartPump — Main Flask application (routes, API calls, database logic)

import os
import requests
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash

# App setup
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "smartpump-dev-key")


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


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
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("cheapest"))


@app.route("/fillup", methods=["GET", "POST"])
def fillup():
    return render_template("fillup.html")


@app.route("/reports", methods=["GET", "POST"])
def reports():
    return render_template("reports.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
