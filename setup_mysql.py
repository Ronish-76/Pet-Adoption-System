#!/usr/bin/env python3
"""
MySQL Database Setup Script for Pet Adoption Platform
Run this script to create the database and setup initial configuration
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # Create database if not exists
        db_name = os.getenv('DB_NAME', 'pet_adoption_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        
        print(f"Database '{db_name}' created successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()