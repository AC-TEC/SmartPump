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
    return render_template("cheapest.html")


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
