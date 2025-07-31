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

def create_shelter_user():
    # Shelter credentials
    username = "happypaws_shelter"
    email = "contact@happypaws.com"
    password = "shelter123"
    first_name = "Happy"
    last_name = "Paws"
    
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
    
    # Update profile to be a shelter
    profile = user.profile
    profile.is_shelter = True
    profile.shelter_name = "Happy Paws Animal Shelter"
    profile.shelter_description = "A loving shelter dedicated to finding homes for abandoned pets"
    profile.phone_number = "+1-555-0123"
    profile.address = "123 Pet Street, Animal City, AC 12345"
    profile.city = "Animal City"
    profile.state = "Animal County"
    profile.zip_code = "12345"
    profile.bio = "We are a non-profit animal shelter that has been serving the community for over 10 years."
    profile.save()
    
    print("\n" + "="*50)
    print("SHELTER USER CREATED SUCCESSFULLY!")
    print("="*50)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    print(f"Shelter Name: {profile.shelter_name}")
    print(f"Phone: {profile.phone_number}")
    print(f"Address: {profile.address}")
    print("="*50)
    print("\nYou can now login to the shelter dashboard with these credentials.")

if __name__ == "__main__":
    create_shelter_user()