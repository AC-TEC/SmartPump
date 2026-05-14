-- SmartPump: SQL queries for cs db course

-- ============================================================
-- PART 1: INSERT STATEMENTS (sample data)
-- ============================================================


-- Users (6 sample users, password hashes generated)
INSERT INTO Users (id, name, email, password_hash, created_at) VALUES
(1, 'Andy Cocha', 'andy.cocha@email.com', 'pbkdf2:sha256:600000$xK9vR3nL$a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2', '2026-01-15 10:30:00'),
(2, 'Maria Santos', 'maria.santos@email.com', 'pbkdf2:sha256:600000$pL8wQ2mJ$b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3', '2026-01-20 14:15:00'),
(3, 'James Carter', 'james.carter@email.com', 'pbkdf2:sha256:600000$mN7xP1kH$c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4', '2026-02-03 09:00:00'),
(4, 'Priya Patel', 'priya.patel@email.com', 'pbkdf2:sha256:600000$jM6yO0iG$d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5', '2026-02-14 11:45:00'),
(5, 'David Kim', 'david.kim@email.com', 'pbkdf2:sha256:600000$hL5zN9fE$e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', '2026-03-01 16:20:00'),
(6, 'Sofia Ramirez', 'sofia.ramirez@email.com', 'pbkdf2:sha256:600000$gK4aM8dD$f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7', '2026-03-10 08:00:00');


-- GasStations (8 sample stations)
INSERT INTO GasStations (id, api_station_id, name, address, city, region, zip_code, rating) VALUES
(1, 210345, 'Costco Gasoline', '2975 Horseblock Rd', 'Medford', 'NY', '11763', 4.5),
(2, 210789, 'BJs Gas', '1100 Sunrise Hwy', 'Bay Shore', 'NY', '11706', 4.2),
(3, 211456, 'Speedway', '455 Commack Rd', 'Deer Park', 'NY', '11729', 3.8),
(4, 212001, 'Shell', '320 Route 110', 'Huntington', 'NY', '11743', 3.5),
(5, 212567, 'Mobil', '890 Jericho Turnpike', 'Smithtown', 'NY', '11787', 3.9),
(6, 213100, 'Gulf', '150 Main St', 'Islip', 'NY', '11751', 3.6),
(7, 213890, 'Sunoco', '2200 Hempstead Tpke', 'East Meadow', 'NY', '11554', 4.0),
(8, 214300, 'Exxon', '505 Montauk Hwy', 'West Babylon', 'NY', '11704', 3.7);


-- FuelTypes (4 standard fuel grades)
INSERT INTO FuelTypes (id, name) VALUES (1, 'Regular');
INSERT INTO FuelTypes (id, name) VALUES (2, 'Midgrade');
INSERT INTO FuelTypes (id, name) VALUES (3, 'Premium');
INSERT INTO FuelTypes (id, name) VALUES (4, 'Diesel');


-- FillUps (20 sample fill-ups across multiple users, stations, and fuel types)
INSERT INTO FillUps (id, user_id, station_id, fuel_type_id, payment_type, gallons, price_per_gallon, total_cost, fill_date) VALUES
(1,  1, 1, 1, 'cash',   12.500, 3.099, 38.74,  '2026-02-01 08:30:00'),
(2,  1, 1, 1, 'cash',   11.200, 3.079, 34.48,  '2026-02-15 09:00:00'),
(3,  1, 3, 1, 'credit', 10.800, 3.299, 35.63,  '2026-03-02 17:45:00'),
(4,  1, 5, 3, 'credit', 13.000, 3.899, 50.69,  '2026-03-20 12:10:00'),
(5,  1, 1, 1, 'cash',   12.000, 3.059, 36.71,  '2026-04-05 08:15:00'),
(6,  2, 2, 1, 'credit', 14.200, 3.199, 45.43,  '2026-02-10 10:30:00'),
(7,  2, 2, 1, 'cash',   13.800, 3.149, 43.46,  '2026-02-28 11:00:00'),
(8,  2, 4, 2, 'credit', 11.500, 3.459, 39.78,  '2026-03-15 14:20:00'),
(9,  2, 7, 1, 'cash',   15.000, 3.189, 47.84,  '2026-04-01 09:45:00'),
(10, 3, 3, 1, 'cash',   10.000, 3.279, 32.79,  '2026-02-20 16:00:00'),
(11, 3, 6, 4, 'credit', 18.500, 3.799, 70.28,  '2026-03-08 07:30:00'),
(12, 3, 8, 1, 'cash',   11.300, 3.259, 36.83,  '2026-03-25 18:15:00'),
(13, 3, 3, 1, 'credit', 10.500, 3.319, 34.85,  '2026-04-10 16:30:00'),
(14, 4, 5, 3, 'credit', 12.800, 3.929, 50.29,  '2026-03-01 13:00:00'),
(15, 4, 7, 3, 'credit', 13.200, 3.959, 52.26,  '2026-03-18 10:00:00'),
(16, 4, 1, 1, 'cash',   14.000, 3.089, 43.25,  '2026-04-02 08:45:00'),
(17, 4, 5, 3, 'credit', 12.500, 3.949, 49.36,  '2026-04-15 12:30:00'),
(18, 5, 8, 1, 'cash',   11.800, 3.239, 38.22,  '2026-03-10 15:00:00'),
(19, 5, 4, 2, 'credit', 10.200, 3.479, 35.49,  '2026-03-28 17:30:00'),
(20, 5, 6, 4, 'credit', 20.000, 3.829, 76.58,  '2026-04-12 07:00:00');


-- UserReportSettings (one row per user, with weekly reports enabled)
INSERT INTO UserReportSettings (id, user_id, weekly_report_enabled) VALUES
(1, 1, TRUE),
(2, 2, TRUE),
(3, 3, FALSE),
(4, 4, TRUE),
(5, 5, FALSE),
(6, 6, FALSE);


-- ============================================================
-- PART 2: SELECT QUERIES
-- ============================================================

-- Query all fill ups for a specific user with station name and fuel type
SELECT f.fill_date, g.name AS station_name, g.address, ft.name AS fuel_type, f.payment_type, f.gallons, f.price_per_gallon, f.total_cost
FROM FillUps f
JOIN GasStations g ON f.station_id = g.id
JOIN FuelTypes ft ON f.fuel_type_id = ft.id
WHERE f.user_id = 1
ORDER BY f.fill_date DESC;


-- Query total spending per user
SELECT u.name, u.email, COUNT(f.id) AS total_fillups, SUM(f.gallons) AS total_gallons, SUM(f.total_cost) AS total_spent
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
