-- Pet Adoption Platform Database Setup
-- Create database
CREATE DATABASE IF NOT EXISTS pet_adoption_db;
USE pet_adoption_db;

-- Create pets table
CREATE TABLE pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    size ENUM('Small', 'Medium', 'Large') NOT NULL,
    description TEXT,
    image VARCHAR(255),
    status ENUM('Available', 'Adopted', 'Pending') DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create users table (for adoption requests)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create adoption_requests table
CREATE TABLE adoption_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    user_id INT,
    applicant_name VARCHAR(100) NOT NULL,
    applicant_email VARCHAR(100) NOT NULL,
    applicant_phone VARCHAR(20),
    message TEXT,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Insert sample pets data
INSERT INTO pets (name, species, breed, age, gender, size, description, image, status) VALUES
('Luna', 'Dog', 'Labrador Retriever', 3, 'Female', 'Large', 'Luna is a friendly and energetic Labrador who loves playing fetch and swimming. She is great with children and other pets.', '../assets/dog1.jpg', 'Available'),
('Max', 'Dog', 'German Shepherd', 5, 'Male', 'Large', 'Max is a loyal and intelligent German Shepherd. He is well-trained and would make an excellent guard dog and family companion.', '../assets/dog2.jpg', 'Available'),
('Bella', 'Cat', 'Persian', 2, 'Female', 'Medium', 'Bella is a beautiful Persian cat with a calm and gentle personality. She loves to be pampered and enjoys quiet environments.', '../assets/cat1.jpg', 'Available'),
('Charlie', 'Dog', 'Golden Retriever', 4, 'Male', 'Large', 'Charlie is a loving Golden Retriever who adores children. He is house-trained and knows basic commands.', '../assets/dog3.jpg', 'Available'),
('Whiskers', 'Cat', 'Tabby', 1, 'Male', 'Small', 'Whiskers is a playful young tabby cat who loves toys and climbing. He would do well in an active household.', '../assets/cat1.jpg', 'Available'),
('Rocky', 'Dog', 'Bulldog', 6, 'Male', 'Medium', 'Rocky is a gentle bulldog with a calm temperament. He enjoys short walks and lots of cuddles on the couch.', '../assets/dog1.jpg', 'Available');

-- Insert sample users
INSERT INTO users (username, email, first_name, last_name, phone) VALUES
('john_doe', 'john@example.com', 'John', 'Doe', '555-0123'),
('jane_smith', 'jane@example.com', 'Jane', 'Smith', '555-0456'),
('mike_wilson', 'mike@example.com', 'Mike', 'Wilson', '555-0789');

-- Insert sample adoption requests
INSERT INTO adoption_requests (pet_id, user_id, applicant_name, applicant_email, applicant_phone, message, status) VALUES
(1, 1, 'John Doe', 'john@example.com', '555-0123', 'I would love to adopt Luna. I have a large backyard and experience with dogs.', 'Pending'),
(3, 2, 'Jane Smith', 'jane@example.com', '555-0456', 'Bella would be perfect for my quiet apartment. I work from home and can give her lots of attention.', 'Approved'),
(2, 3, 'Mike Wilson', 'mike@example.com', '555-0789', 'Max seems like the perfect guard dog for my family. We have children who would love him.', 'Pending');