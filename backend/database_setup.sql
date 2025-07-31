-- MySQL Database Setup for Pet Adoption Platform
-- Run this script in MySQL to create the database and tables

CREATE DATABASE IF NOT EXISTS pet_adoption_db;
USE pet_adoption_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shelters table
CREATE TABLE IF NOT EXISTS shelters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pets table
CREATE TABLE IF NOT EXISTS pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    pet_type ENUM('dog', 'cat', 'bird', 'rabbit', 'other') NOT NULL,
    breed VARCHAR(50),
    age INT,
    gender ENUM('male', 'female') NOT NULL,
    size ENUM('small', 'medium', 'large') NOT NULL,
    description TEXT,
    image LONGTEXT,
    status ENUM('available', 'adopted', 'pending') DEFAULT 'available',
    shelter_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shelter_id) REFERENCES shelters(id) ON DELETE CASCADE
);

-- Adoption requests table
CREATE TABLE IF NOT EXISTS adoption_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    pet_id INT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_date TIMESTAMP NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
);

-- Insert sample shelter
INSERT INTO shelters (name, email, password, phone, address) VALUES 
('Happy Paws Shelter', 'shelter@example.com', 'shelter123', '555-0123', '123 Pet Street, City, State');

-- Insert sample pets
INSERT INTO pets (name, pet_type, breed, age, gender, size, description, status, shelter_id) VALUES 
('Buddy', 'dog', 'Golden Retriever', 3, 'male', 'large', 'Friendly and energetic dog looking for a loving home.', 'available', 1),
('Luna', 'cat', 'Persian', 2, 'female', 'medium', 'Calm and affectionate cat who loves to cuddle.', 'available', 1),
('Max', 'dog', 'German Shepherd', 4, 'male', 'large', 'Loyal and protective dog, great with families.', 'available', 1),
('Bella', 'cat', 'Siamese', 1, 'female', 'small', 'Playful kitten with beautiful blue eyes.', 'available', 1),
('Charlie', 'dog', 'Labrador', 5, 'male', 'large', 'Gentle giant who loves children and other pets.', 'available', 1),
('Mia', 'cat', 'Maine Coon', 3, 'female', 'large', 'Fluffy and friendly cat with a gentle personality.', 'available', 1);

-- Insert sample user
INSERT INTO users (username, email, password, full_name, phone, address) VALUES 
('john_doe', 'john@example.com', 'password123', 'John Doe', '555-0456', '456 User Avenue, City, State');