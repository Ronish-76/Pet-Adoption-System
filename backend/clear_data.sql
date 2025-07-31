-- Clear all pets and adoption data to start fresh
USE pet_adoption_db;

-- Delete all data from related tables (order matters due to foreign keys)
DELETE FROM adoption_requests;
DELETE FROM favorites;
DELETE FROM notifications;
DELETE FROM pet_medical_info;
DELETE FROM pets;

-- Reset auto-increment counters
ALTER TABLE adoption_requests AUTO_INCREMENT = 1;
ALTER TABLE favorites AUTO_INCREMENT = 1;
ALTER TABLE notifications AUTO_INCREMENT = 1;
ALTER TABLE pet_medical_info AUTO_INCREMENT = 1;
ALTER TABLE pets AUTO_INCREMENT = 1;

-- Keep shelters and users for login functionality
-- DELETE FROM shelters;
-- DELETE FROM users;