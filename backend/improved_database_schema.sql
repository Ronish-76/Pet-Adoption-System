-- Enhanced database schema with missing tables and improvements
USE pet_adoption_db;

-- Add missing tables for better functionality

-- Favorites table - users can save favorite pets
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    pet_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, pet_id)
);

-- Notifications table - system notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Pet medical info table - separate health records
CREATE TABLE IF NOT EXISTS pet_medical_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT,
    vaccination_status ENUM('up_to_date', 'partial', 'none') DEFAULT 'none',
    spayed_neutered BOOLEAN DEFAULT FALSE,
    medical_notes TEXT,
    last_checkup DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
);

-- Audit logs table - track important actions
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_type ENUM('user', 'shelter', 'admin') NOT NULL,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    old_values JSON,
    new_values JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for better performance
CREATE INDEX idx_pets_status ON pets(status);
CREATE INDEX idx_pets_type ON pets(pet_type);
CREATE INDEX idx_adoption_status ON adoption_requests(status);
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_shelter_email ON shelters(email);

-- Add soft delete column (optional)
ALTER TABLE pets ADD COLUMN deleted_at TIMESTAMP NULL;
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP NULL;
ALTER TABLE shelters ADD COLUMN deleted_at TIMESTAMP NULL;