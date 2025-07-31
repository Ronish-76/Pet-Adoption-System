import sqlite3
import os

# Create SQLite database for development
db_path = 'pet_adoption.db'

# Remove existing database
if os.path.exists(db_path):
    os.remove(db_path)

# Create new database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create pets table
cursor.execute('''
CREATE TABLE pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    size TEXT NOT NULL,
    description TEXT,
    image TEXT,
    status TEXT DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create adoption_requests table
cursor.execute('''
CREATE TABLE adoption_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    applicant_name TEXT NOT NULL,
    applicant_email TEXT NOT NULL,
    applicant_phone TEXT,
    message TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
)
''')

# Insert sample pets
pets_data = [
    ('Luna', 'Dog', 'Labrador Retriever', 3, 'Female', 'Large', 'Luna is a friendly and energetic Labrador who loves playing fetch and swimming.', '../assets/dog1.jpg', 'Available'),
    ('Max', 'Dog', 'German Shepherd', 5, 'Male', 'Large', 'Max is a loyal and intelligent German Shepherd. He is well-trained and would make an excellent guard dog.', '../assets/dog2.jpg', 'Available'),
    ('Bella', 'Cat', 'Persian', 2, 'Female', 'Medium', 'Bella is a beautiful Persian cat with a calm and gentle personality.', '../assets/cat1.jpg', 'Available'),
    ('Charlie', 'Dog', 'Golden Retriever', 4, 'Male', 'Large', 'Charlie is a loving Golden Retriever who adores children.', '../assets/dog3.jpg', 'Available'),
    ('Whiskers', 'Cat', 'Tabby', 1, 'Male', 'Small', 'Whiskers is a playful young tabby cat who loves toys and climbing.', '../assets/cat1.jpg', 'Available'),
    ('Rocky', 'Dog', 'Bulldog', 6, 'Male', 'Medium', 'Rocky is a gentle bulldog with a calm temperament.', '../assets/dog1.jpg', 'Available')
]

cursor.executemany('''
INSERT INTO pets (name, species, breed, age, gender, size, description, image, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', pets_data)

# Insert sample adoption requests
adoption_data = [
    (1, 'John Doe', 'john@example.com', '555-0123', 'I would love to adopt Luna. I have a large backyard and experience with dogs.', 'Pending'),
    (3, 'Jane Smith', 'jane@example.com', '555-0456', 'Bella would be perfect for my quiet apartment.', 'Approved'),
    (2, 'Mike Wilson', 'mike@example.com', '555-0789', 'Max seems like the perfect guard dog for my family.', 'Pending')
]

cursor.executemany('''
INSERT INTO adoption_requests (pet_id, applicant_name, applicant_email, applicant_phone, message, status)
VALUES (?, ?, ?, ?, ?, ?)
''', adoption_data)

conn.commit()

# Test the database
cursor.execute("SELECT COUNT(*) FROM pets")
pet_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM adoption_requests")
adoption_count = cursor.fetchone()[0]

print(f"Database created successfully!")
print(f"Total pets: {pet_count}")
print(f"Total adoption requests: {adoption_count}")

conn.close()
print("SQLite database 'pet_adoption.db' created successfully!")