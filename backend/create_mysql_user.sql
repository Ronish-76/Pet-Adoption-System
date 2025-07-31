-- Create secure MySQL user for production
CREATE USER 'adoption_admin'@'localhost' IDENTIFIED BY 'SecurePet2024!';
GRANT SELECT, INSERT, UPDATE, DELETE ON pet_adoption_db.* TO 'adoption_admin'@'localhost';
FLUSH PRIVILEGES;