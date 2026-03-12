-- =============================
-- USERS TABLE
-- =============================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(20) DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================
-- CARS TABLE
-- =============================
CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price_per_day DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

-- =============================
-- BOOKINGS TABLE
-- =============================
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    car_id INTEGER,
    start_date DATE,
    end_date DATE,
    total_price DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (car_id) REFERENCES cars(id)
);

-- =============================
-- PAYMENTS TABLE
-- =============================
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending',
    paid_at TIMESTAMP,

    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

-- =============================
-- RENTALS TABLE
-- =============================
CREATE TABLE rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    pickup_time TIMESTAMP,
    return_time TIMESTAMP,
    fuel_level_start VARCHAR(20),
    fuel_level_end VARCHAR(20),
    extra_charges DECIMAL(10,2) DEFAULT 0,

    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);