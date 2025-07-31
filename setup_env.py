#!/usr/bin/env python
"""
Setup environment variables for Pet Adoption Platform
"""

import os

def create_env_file():
    """Create .env file with MySQL configuration"""
    env_content = """# Pet Adoption Platform Environment Variables
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-key-2024

# MySQL Database Configuration
DB_NAME=pet_adoption_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

# Optional: Customize these values if needed
# DB_PASSWORD=your_mysql_password
# DB_HOST=127.0.0.1
"""

    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("📝 Please edit the .env file and update your MySQL credentials if needed:")
    print("   - DB_PASSWORD: Your MySQL root password")
    print("   - DB_HOST: MySQL host (default: localhost)")
    print("   - DB_PORT: MySQL port (default: 3306)")

if __name__ == "__main__":
    create_env_file() 