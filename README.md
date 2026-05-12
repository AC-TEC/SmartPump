# SmartPump

A web app that helps drivers find the cheapest gas nearby, log their fill-ups, and receive automated weekly spending reports via email.

**Live Demo:** [smartpump-production.up.railway.app](https://smartpump-production.up.railway.app)

---

## Features

- **Search gas prices** by zip code, city name, or GPS coordinates
- **Filter by fuel type** — Regular, Midgrade, Premium, Diesel
- **Filter by payment method** — Cash or Credit (shows the best price), Credit Only
- **Results sorted cheapest first** with station name, address, rating, and price
- **Log fill-ups** with pre-filled station data, payment selection, and auto-calculated totals
- **Email CSV reports** — get your fill-up history for the current week or a custom date range
- **Automated weekly reports** — opt in to receive a report every Monday via email
- **User accounts** with secure password hashing

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python  |
| Web Framework | Flask |
| Database | MySQL (hosted on Railway) |
| Gas Price API | Apify FuelPrices (`johnvc/fuelprices`) |
| Email Delivery | Resend |
| Hosting | Railway |
| Cron Jobs | Railway Cron Service |

---

## Database Schema

**5 tables:**

| Table | Role |
|-------|------|
| **Users** | Registered users (name, email, password hash) |
| **GasStations** | Stations where users have filled up (populated on fill-up, not on every API call) |
| **FuelTypes** | Regular, Midgrade, Premium, Diesel (seeded data, IDs match API given value) |
| **FillUps** | User gas purchase log (station, fuel type, payment type, gallons, price, total) |
| **UserReportSettings** | Per-user toggle for automated weekly email reports |

**Relationships:**

```
Users (1) → (many) FillUps
Users (1) → (1)  UserReportSettings
GasStations (1) → (many) FillUps
FuelTypes (1) → (many) FillUps
```

---

## Project Structure

```
SmartPump/
├── app.py                  — Main Flask application (routes, API calls, database logic)
├── cron_report.py          — Weekly automated report script (Railway cron runs this)
├── schema.sql              — Database schema (CREATE TABLE statements for all 5 tables)
├── seed.sql                — Seed data (initial FuelTypes records)
├── queries.sql             — SQL queries
├── setup_db.py             — One time script to create tables and seed data on Railway MySQL
├── requirements.txt        — Python dependencies
├── Procfile                — Railway deployment config (gunicorn)
├── static/
│   ├── style.css           — Styling
│   └── logo.png            — SmartPump logo
└── templates/
    ├── base.html           — Shared layout (nav bar, flash messages)
    ├── cheapest.html       — Gas price search and results
    ├── signup.html         — User registration
    ├── login.html          — User login
    ├── fillup.html         — Log fill-up form
    └── reports.html        — Email reports and weekly toggle
```
