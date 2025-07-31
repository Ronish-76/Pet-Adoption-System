#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def create_test_user():
    # Test user credentials
    username = "testuser"
    email = "test@example.com"
    password = "test123"
    first_name = "Test"
    last_name = "User"
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists!")
        user = User.objects.get(username=username)
    else:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        print(f"Created user: {username}")
    
    # Update profile
    profile = user.profile
    profile.is_shelter = False
    profile.phone_number = "+1-555-0456"
    profile.address = "456 Test Street, Test City, TC 67890"
    profile.city = "Test City"
    profile.state = "Test State"
    profile.zip_code = "67890"
    profile.bio = "I love pets and want to adopt one!"
    profile.save()
    
    print("\n" + "="*50)
    print("TEST USER CREATED SUCCESSFULLY!")
    print("="*50)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    print("="*50)
    print("\nYou can now login and test pet adoption with these credentials.")

if __name__ == "__main__":
    create_test_user()