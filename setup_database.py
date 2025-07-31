#!/usr/bin/env python3
"""
Database setup script for Pet Adoption Platform
Run this script to create and populate the MySQL database
"""

import mysql.connector
from mysql.connector import Error
import os

def create_database():
    """Create database and tables"""
    connection = None
    try:
        # Database connection parameters
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
        }
        
        # Connect to MySQL server
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Read and execute SQL file
        with open('database_setup.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        
        # Split SQL script into individual statements
        sql_commands = sql_script.split(';')
        
        for command in sql_commands:
            command = command.strip()
            if command:
                cursor.execute(command)
        
        connection.commit()
        print("Database created successfully!")
        print("Tables created successfully!")
        print("Sample data inserted successfully!")
        
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def test_connection():
    """Test database connection"""
    connection = None
    try:
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'pet_adoption_db'
        }
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM pets")
        pet_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adoption_requests")
        adoption_count = cursor.fetchone()[0]
        
        print(f"Database connection successful!")
        print(f"Total pets in database: {pet_count}")
        print(f"Total adoption requests: {adoption_count}")
        
    except Error as e:
        print(f"Connection test failed: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("Pet Adoption Platform - Database Setup")
    print("=" * 50)
    
    # Check if SQL file exists
    if not os.path.exists('database_setup.sql'):
        print("database_setup.sql file not found!")
        exit(1)
    
    # Create database
    create_database()
    
    # Test connection
    print("\n" + "=" * 50)
    print("Testing database connection...")
    test_connection()
    
    print("\nDatabase setup complete!")
    print("You can now run your Django application.")