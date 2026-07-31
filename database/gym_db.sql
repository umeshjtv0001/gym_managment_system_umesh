CREATE DATABASE IF NOT EXISTS gym_db;

USE gym_db;

CREATE TABLE users(
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(50),
password VARCHAR(100)
);

INSERT INTO users(username,password)
VALUES('admin','admin123');

CREATE TABLE members(
member_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
age INT,
gender VARCHAR(20),
phone VARCHAR(20),
email VARCHAR(100),
address TEXT,
join_date DATE
);

CREATE TABLE plans(
plan_id INT AUTO_INCREMENT PRIMARY KEY,
plan_name VARCHAR(50),
duration INT,
price DECIMAL(10,2)
);

CREATE TABLE subscriptions(
subscription_id INT AUTO_INCREMENT PRIMARY KEY,
member_id INT,
plan_id INT,
start_date DATE,
end_date DATE,
status VARCHAR(20),
FOREIGN KEY(member_id) REFERENCES members(member_id),
FOREIGN KEY(plan_id) REFERENCES plans(plan_id)
);

CREATE TABLE payments(
payment_id INT AUTO_INCREMENT PRIMARY KEY,
member_id INT,
amount DECIMAL(10,2),
payment_date DATE,
payment_method VARCHAR(30),
FOREIGN KEY(member_id) REFERENCES members(member_id)
);

CREATE TABLE attendance(
attendance_id INT AUTO_INCREMENT PRIMARY KEY,
member_id INT,
attendance_date DATE,
status VARCHAR(20),
FOREIGN KEY(member_id) REFERENCES members(member_id)
);