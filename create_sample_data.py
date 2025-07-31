#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from pets.models import Pet
from adoption.models import AdoptionRequest
from accounts.models import UserProfile

def create_sample_data():
    print("Creating sample data...")
    
    # Create users
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@pawmatch.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        admin_user.profile.is_shelter = True
        admin_user.profile.shelter_name = 'PawMatch Shelter'
        admin_user.profile.save()
    
    # Create regular users
    users_data = [
        {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('password123')
            user.save()
    
    # Create pets
    pets_data = [
        {
            'name': 'Buddy',
            'pet_type': 'dog',
            'breed': 'Golden Retriever',
            'age': 3,
            'gender': 'male',
            'description': 'Friendly and energetic dog, great with kids.',
            'status': 'available'
        },
        {
            'name': 'Whiskers',
            'pet_type': 'cat',
            'breed': 'Persian',
            'age': 2,
            'gender': 'female',
            'description': 'Calm and affectionate cat, loves to cuddle.',
            'status': 'available'
        },
        {
            'name': 'Max',
            'pet_type': 'dog',
            'breed': 'German Shepherd',
            'age': 5,
            'gender': 'male',
            'description': 'Loyal and protective, well-trained.',
            'status': 'available'
        },
        {
            'name': 'Luna',
            'pet_type': 'cat',
            'breed': 'Siamese',
            'age': 1,
            'gender': 'female',
            'description': 'Playful kitten, very social.',
            'status': 'available'
        },
        {
            'name': 'Charlie',
            'pet_type': 'dog',
            'breed': 'Labrador',
            'age': 4,
            'gender': 'male',
            'description': 'Great family dog, loves swimming.',
            'status': 'adopted'
        }
    ]
    
    for pet_data in pets_data:
        pet, created = Pet.objects.get_or_create(
            name=pet_data['name'],
            defaults={**pet_data, 'owner': admin_user}
        )
        if created:
            print(f"Created pet: {pet.name}")
    
    # Create adoption requests
    john = User.objects.get(username='john_doe')
    jane = User.objects.get(username='jane_smith')
    buddy = Pet.objects.get(name='Buddy')
    whiskers = Pet.objects.get(name='Whiskers')
    
    adoption_requests = [
        {
            'user': john,
            'pet': buddy,
            'reason': 'I have a large backyard and love active dogs. Buddy would be perfect for my family.',
            'status': 'pending'
        },
        {
            'user': jane,
            'pet': whiskers,
            'reason': 'I work from home and would love a calm companion. I have experience with cats.',
            'status': 'approved'
        }
    ]
    
    for req_data in adoption_requests:
        request, created = AdoptionRequest.objects.get_or_create(
            user=req_data['user'],
            pet=req_data['pet'],
            defaults=req_data
        )
        if created:
            print(f"Created adoption request: {request.user.username} -> {request.pet.name}")
    
    print("Sample data created successfully!")
    print("\nDatabase Summary:")
    print(f"Users: {User.objects.count()}")
    print(f"Pets: {Pet.objects.count()}")
    print(f"Adoption Requests: {AdoptionRequest.objects.count()}")

if __name__ == '__main__':
    create_sample_data()