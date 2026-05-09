-- SmartPump — Database schema (CREATE TABLE statements for all 5 tables)

-- Table 1: Users
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: GasStations
CREATE TABLE GasStations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    api_station_id INT NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    rating DECIMAL(2,1)
);

-- Table 3: FuelTypes
CREATE TABLE FuelTypes (
    id INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);

-- Table 4: FillUps
CREATE TABLE FillUps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    station_id INT NOT NULL,
    fuel_type_id INT NOT NULL,
    payment_type ENUM('cash', 'credit') NOT NULL,
    gallons DECIMAL(6,3) NOT NULL,
    price_per_gallon DECIMAL(5,3) NOT NULL,
    total_cost DECIMAL(7,2) NOT NULL,
    fill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (station_id) REFERENCES GasStations(id),
    FOREIGN KEY (fuel_type_id) REFERENCES FuelTypes(id)
);

-- Table 5: UserReportSettings
CREATE TABLE UserReportSettings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    weekly_report_enabled BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
