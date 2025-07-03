CREATE DATABASE IF NOT EXISTS battery_swap;
USE battery_swap;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL
);

CREATE TABLE bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  station VARCHAR(100),
  date DATE,
  FOREIGN KEY (username) REFERENCES users(username)
);
ALTER TABLE bookings ADD COLUMN status VARCHAR(20) DEFAULT 'Pending';
SELECT *FROM users;