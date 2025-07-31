#!/usr/bin/env python3
"""
Fix .env file with correct MySQL configuration
"""

def fix_env_file():
    """Fix the .env file with correct MySQL settings"""
    env_content = """# Pet Adoption Platform Environment Variables
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-key-2024

# MySQL Database Configuration
DB_NAME=pet_adoption_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file fixed with correct MySQL configuration!")
    print("📋 Configuration:")
    print("   Host: localhost")
    print("   Port: 3306")
    print("   Password: (no password)")
    print("   Database: pet_adoption_db")

if __name__ == "__main__":
    fix_env_file() 