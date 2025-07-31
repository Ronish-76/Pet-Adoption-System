#!/usr/bin/env python3
"""
MySQL Configuration Helper for Pet Adoption Platform
This script helps you configure MySQL connection settings
"""

import os
import getpass
from dotenv import load_dotenv

def configure_mysql():
    """Configure MySQL connection settings"""
    print("🐾 MySQL Configuration for Pet Adoption Platform")
    print("=" * 50)
    
    # Load existing .env if it exists
    load_dotenv()
    
    # Get current settings
    current_password = os.getenv('DB_PASSWORD', '')
    current_host = os.getenv('DB_HOST', 'localhost')
    current_port = os.getenv('DB_PORT', '3306')
    
    print(f"Current settings:")
    print(f"  Host: {current_host}")
    print(f"  Port: {current_port}")
    print(f"  Password: {'*' * len(current_password) if current_password else '(not set)'}")
    
    print("\n📝 Please provide your MySQL configuration:")
    
    # Get MySQL password
    password = getpass.getpass("MySQL root password (press Enter if no password): ")
    if not password:
        password = ""
    
    # Get host (optional)
    host = input(f"MySQL host (default: {current_host}): ").strip()
    if not host:
        host = current_host
    
    # Get port (optional)
    port = input(f"MySQL port (default: {current_port}): ").strip()
    if not port:
        port = current_port
    
    # Update .env file
    env_content = f"""# Pet Adoption Platform Environment Variables
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-key-2024

# MySQL Database Configuration
DB_NAME=pet_adoption_db
DB_USER=root
DB_PASSWORD={password}
DB_HOST={host}
DB_PORT={port}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file updated successfully!")
    print(f"📋 Configuration saved:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Password: {'*' * len(password) if password else '(no password)'}")
    
    # Test connection
    print("\n🔍 Testing MySQL connection...")
    try:
        import mysql.connector
        
        connection = mysql.connector.connect(
            host=host,
            user='root',
            password=password,
            port=int(port)
        )
        
        if connection.is_connected():
            print("✅ MySQL connection successful!")
            
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS pet_adoption_db")
            print("✅ Database 'pet_adoption_db' created/verified!")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 MySQL is ready for the Pet Adoption Platform!")
            print("Next steps:")
            print("1. Run: python manage.py migrate")
            print("2. Run: python manage.py createsuperuser")
            print("3. Run: python create_sample_data.py")
            print("4. Run: python manage.py runserver 8000")
            
        else:
            print("❌ MySQL connection failed!")
            
    except ImportError:
        print("❌ mysql-connector-python not installed. Installing...")
        os.system("pip install mysql-connector-python")
        print("✅ Please run this script again after installation.")
        
    except Exception as e:
        print(f"❌ MySQL connection error: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure MySQL is running")
        print("2. Check if the password is correct")
        print("3. If using XAMPP, check XAMPP Control Panel")
        print("4. Try connecting with: mysql -u root -p")

if __name__ == "__main__":
    configure_mysql() 