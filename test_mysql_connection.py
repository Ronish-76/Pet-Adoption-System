#!/usr/bin/env python3
"""
Test MySQL connection with different configurations
"""

import mysql.connector
import os
from dotenv import load_dotenv

def test_mysql_connection():
    """Test MySQL connection with different configurations"""
    print("🔍 Testing MySQL Connection...")
    print("=" * 40)
    
    # Common MySQL passwords to try
    common_passwords = [
        "",  # No password
        "root",
        "password",
        "admin",
        "123456",
        "mysql",
        "xampp",
        "wamp"
    ]
    
    host = "localhost"
    port = 3306
    
    for password in common_passwords:
        try:
            print(f"Testing with password: {'(empty)' if password == '' else password}")
            
            connection = mysql.connector.connect(
                host=host,
                user='root',
                password=password,
                port=port
            )
            
            if connection.is_connected():
                print(f"✅ SUCCESS! Password found: {'(empty)' if password == '' else password}")
                
                cursor = connection.cursor()
                
                # Create database
                cursor.execute("CREATE DATABASE IF NOT EXISTS pet_adoption_db")
                print("✅ Database 'pet_adoption_db' created/verified!")
                
                cursor.close()
                connection.close()
                
                # Update .env file with correct password
                env_content = f"""# Pet Adoption Platform Environment Variables
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-key-2024

# MySQL Database Configuration
DB_NAME=pet_adoption_db
DB_USER=root
DB_PASSWORD={password}
DB_HOST=localhost
DB_PORT=3306
"""
                
                with open('.env', 'w') as f:
                    f.write(env_content)
                
                print(f"✅ .env file updated with correct password!")
                print("\n🎉 MySQL is ready! Next steps:")
                print("1. Run: python manage.py migrate")
                print("2. Run: python manage.py createsuperuser")
                print("3. Run: python create_sample_data.py")
                print("4. Run: python manage.py runserver 8000")
                
                return True
                
        except mysql.connector.Error as err:
            if err.errno == 1045:  # Access denied
                print(f"❌ Access denied with password: {'(empty)' if password == '' else password}")
            else:
                print(f"❌ Error: {err}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    print("\n❌ Could not connect with any common password.")
    print("\n🔧 Manual setup required:")
    print("1. Find your MySQL root password")
    print("2. Edit .env file manually")
    print("3. Set DB_PASSWORD=your_actual_password")
    print("\n💡 Common places to find MySQL password:")
    print("- XAMPP Control Panel")
    print("- WAMP settings")
    print("- MySQL installation notes")
    print("- Try: mysql -u root -p")
    
    return False

if __name__ == "__main__":
    test_mysql_connection() 