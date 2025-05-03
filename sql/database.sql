CREATE DATABASE IF NOT EXISTS s3_mrs;
USE s3_mrs;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_code INT NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('student','lecturer','admin','it','technician') NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_code VARCHAR(20) NOT NULL UNIQUE,
    room_type ENUM('individual', 'group', 'mentoring') NOT NULL,
    location VARCHAR(100) NOT NULL,
    status ENUM('available', 'in_use', 'maintenance') NOT NULL,
    sensor ENUM('active', 'inactive') NOT NULL
);

CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('light', 'fan', 'air_conditioner') NOT NULL,
    status ENUM('on', 'off', 'error') NOT NULL,
    room_id INT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    booking_date DATE NOT NULL ,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status ENUM('active', 'cancelled', 'checked_in', 'checked_out') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

CREATE TABLE checkin_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    checkin_time DATETIME,
    checkout_time DATETIME,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

INSERT INTO `rooms` (`id`, `room_code`, `room_type`, `location`, `status`, `sensor`) VALUES
(1, 'H1_101', 'group', 'tòa H1, tầng 1', 'available', 'inactive'),
(2, 'H2_301', 'mentoring', 'tòa H2, tầng 3', 'available', 'inactive');
