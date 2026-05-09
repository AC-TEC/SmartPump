# SmartPump — One-time database setup script (creates tables and seeds data)

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = connection.cursor()

# Run schema.sql
print("Creating tables...")
with open("schema.sql", "r") as schema_file:
    sql = schema_file.read()

for statement in sql.split(";"):
    statement = statement.strip()
    if statement:
        cursor.execute(statement)

print("Tables created successfully.")

# Run seed.sql
print("Seeding fuel types...")
with open("seed.sql", "r") as seed_file:
    sql = seed_file.read()

for statement in sql.split(";"):
    statement = statement.strip()
    if statement:
        cursor.execute(statement)

connection.commit()
print("Seed data inserted successfully.")

cursor.close()
connection.close()
print("Done! Database is ready.")
