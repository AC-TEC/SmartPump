# SmartPump — Weekly automated report script (Railway cron runs this)

import os
import csv
import io
import resend
import mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


def generate_csv(fillups):
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
    return csv_content


def send_report(user_name, user_email, csv_content, start_date, end_date):
    filename = f"smartpump_report_{start_date}_to_{end_date}.csv"

    resend.Emails.send({
        "from": "SmartPump <onboarding@resend.dev>",
        "to": [user_email],
        "subject": f"SmartPump — Your Weekly Gas Spending Report ({start_date} to {end_date})",
        "html": f"<p>Hi {user_name}!</p><p>Here's your automated weekly fill-up report for {start_date} to {end_date}.</p><p>— SmartPump</p>",
        "attachments": [{"filename": filename, "content": list(csv_content.encode("utf-8"))}]
    })


def run_weekly_reports():
    today = datetime.utcnow()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    start_date = last_monday.strftime("%Y-%m-%d")
    end_date = last_sunday.strftime("%Y-%m-%d")

    print(f"Generating weekly reports for {start_date} to {end_date}...")

    connection = get_db()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT u.id, u.name, u.email
        FROM Users u
        JOIN UserReportSettings urs ON u.id = urs.user_id
        WHERE urs.weekly_report_enabled = true
    """)
    enabled_users = cursor.fetchall()

    print(f"Found {len(enabled_users)} user(s) with weekly reports enabled.")

    for user in enabled_users:
        cursor.execute("""
            SELECT f.fill_date, g.name AS station, g.address, ft.name AS fuel_type,
                   f.payment_type, f.gallons, f.price_per_gallon, f.total_cost
            FROM FillUps f
            JOIN GasStations g ON f.station_id = g.id
            JOIN FuelTypes ft ON f.fuel_type_id = ft.id
            WHERE f.user_id = %s AND DATE(f.fill_date) BETWEEN %s AND %s
            ORDER BY f.fill_date
        """, (user["id"], start_date, end_date))
        fillups = cursor.fetchall()

        if not fillups:
            print(f"  {user['name']} ({user['email']}): No fill-ups last week — skipping.")
            continue

        csv_content = generate_csv(fillups)
        send_report(user["name"], user["email"], csv_content, start_date, end_date)
        print(f"  {user['name']} ({user['email']}): Report sent ({len(fillups)} fill-ups).")

    cursor.close()
    connection.close()
    print("Done.")


if __name__ == "__main__":
    run_weekly_reports()
