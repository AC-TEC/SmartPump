-- SmartPump — SQL queries for cs db course

-- Query all fill-ups for a specific user with station name and fuel type
SELECT f.fill_date, g.name AS station_name, g.address, ft.name AS fuel_type, f.payment_type, f.gallons, f.price_per_gallon, f.total_cost
FROM FillUps f
JOIN GasStations g ON f.station_id = g.id
JOIN FuelTypes ft ON f.fuel_type_id = ft.id
WHERE f.user_id = 1
ORDER BY f.fill_date DESC;


-- Query total spending per user
SELECT u.name, u.email, COUNT(f.id) AS total_fillups,
       SUM(f.gallons) AS total_gallons, SUM(f.total_cost) AS total_spent
FROM Users u
JOIN FillUps f ON u.id = f.user_id
GROUP BY u.id, u.name, u.email
ORDER BY total_spent DESC;


-- Query most visited gas station per user
SELECT u.name AS user_name, g.name AS station_name, g.address, COUNT(f.id) AS visit_count
FROM FillUps f
JOIN Users u ON f.user_id = u.id
JOIN GasStations g ON f.station_id = g.id
GROUP BY u.id, u.name, g.id, g.name, g.address
ORDER BY u.name, visit_count DESC;


-- Query users who have weekly reports enabled
SELECT u.name, u.email, urs.weekly_report_enabled
FROM Users u
JOIN UserReportSettings urs ON u.id = urs.user_id
WHERE urs.weekly_report_enabled = true
ORDER BY u.name;


-- Query the single most expensive fill-up
SELECT u.name AS user_name, g.name AS station_name, ft.name AS fuel_type, f.payment_type, f.gallons, f.price_per_gallon, f.total_cost, f.fill_date
FROM FillUps f
JOIN Users u ON f.user_id = u.id
JOIN GasStations g ON f.station_id = g.id
JOIN FuelTypes ft ON f.fuel_type_id = ft.id
ORDER BY f.total_cost DESC
LIMIT 1;


-- Query users who have never logged a fill-up
SELECT u.name, u.email, u.created_at
FROM Users u
LEFT JOIN FillUps f ON u.id = f.user_id
WHERE f.id IS NULL
ORDER BY u.created_at;
