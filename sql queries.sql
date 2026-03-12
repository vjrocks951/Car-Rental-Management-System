-- Get all available cars
SELECT * FROM cars WHERE is_available = TRUE;

-- Get bookings of a user
SELECT * FROM bookings WHERE user_id = 1;

-- Total revenue
SELECT SUM(amount) FROM payments WHERE payment_status = 'completed';

-- Booking details with user & car
SELECT b.id, u.name, c.brand, c.model, b.start_date, b.end_date
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN cars c ON b.car_id = c.id;