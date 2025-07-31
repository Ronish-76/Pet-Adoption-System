#!/usr/bin/env python
"""
Startup script for Pet Adoption Platform
This script handles database setup and server startup
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(e.stderr)
        return False

def setup_database():
    """Setup database and run migrations"""
    print("Setting up database...")
    
    # Check if migrations exist
    migrations_exist = any(
        (BASE_DIR / app / 'migrations').exists() 
        for app in ['accounts', 'pets', 'adoption', 'chat']
    )
    
    if not migrations_exist:
        print("Creating initial migrations...")
        run_command("python manage.py makemigrations accounts", "Creating accounts migrations")
        run_command("python manage.py makemigrations pets", "Creating pets migrations")
        run_command("python manage.py makemigrations adoption", "Creating adoption migrations")
        run_command("python manage.py makemigrations chat", "Creating chat migrations")
    
    # Run migrations
    run_command("python manage.py migrate", "Running database migrations")
    
    # Create superuser if it doesn't exist
    try:
        django.setup()
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("Creating superuser...")
            run_command(
                'python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'admin@example.com\', \'admin123\')"',
                "Creating superuser (admin/admin123)"
            )
    except Exception as e:
        print(f"Note: Could not create superuser automatically: {e}")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")

def start_server():
    """Start the Django development server"""
    print("\n" + "="*50)
    print("🚀 Starting Pet Adoption Platform Server")
    print("="*50)
    print("Server will be available at: http://localhost:8000")
    print("Admin panel: http://localhost:8000/admin")
    print("API documentation: http://localhost:8000/swagger/")
    print("Press Ctrl+C to stop the server")
    print("="*50)
    
    try:
        subprocess.run(["python", "manage.py", "runserver", "8000"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")

def main():
    """Main function"""
    print("🐾 Pet Adoption Platform Setup")
    print("="*40)
    
    # Check if we're in the right directory
    if not (BASE_DIR / 'manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Setup database
    setup_database()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()