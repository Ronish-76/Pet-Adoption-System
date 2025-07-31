#!/usr/bin/env python
"""
Database Status Checker for Pet Adoption Platform
Shows all data in the database
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from pets.models import Pet
from adoption.models import AdoptionRequest
from chat.models import Message

def print_separator(title):
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60)

def check_users():
    print_separator("USERS & PROFILES")
    users = User.objects.all().select_related('profile')
    
    if not users.exists():
        print("No users found in database.")
        return
    
    print(f"Total Users: {users.count()}")
    print("\nUser Details:")
    print("-" * 80)
    print(f"{'ID':<3} {'Username':<15} {'Email':<25} {'Name':<20} {'Shelter':<8} {'Shelter Name':<20}")
    print("-" * 80)
    
    for user in users:
        profile = getattr(user, 'profile', None)
        is_shelter = "Yes" if profile and profile.is_shelter else "No"
        shelter_name = profile.shelter_name if profile and profile.is_shelter else "-"
        full_name = f"{user.first_name} {user.last_name}".strip() or "-"
        
        print(f"{user.id:<3} {user.username:<15} {user.email:<25} {full_name:<20} {is_shelter:<8} {shelter_name:<20}")

def check_pets():
    print_separator("PETS")
    pets = Pet.objects.all().select_related('owner', 'owner__profile')
    
    if not pets.exists():
        print("No pets found in database.")
        return
    
    print(f"Total Pets: {pets.count()}")
    print("\nPet Details:")
    print("-" * 100)
    print(f"{'ID':<3} {'Name':<15} {'Type':<10} {'Breed':<15} {'Age':<5} {'Status':<12} {'Owner':<15} {'Shelter':<20}")
    print("-" * 100)
    
    for pet in pets:
        owner_name = pet.owner.username if pet.owner else "None"
        shelter_name = pet.owner.profile.shelter_name if pet.owner and hasattr(pet.owner, 'profile') and pet.owner.profile.is_shelter else "-"
        
        print(f"{pet.id:<3} {pet.name:<15} {pet.pet_type:<10} {pet.breed:<15} {pet.age:<5} {pet.status:<12} {owner_name:<15} {shelter_name:<20}")

def check_adoption_requests():
    print_separator("ADOPTION REQUESTS")
    requests = AdoptionRequest.objects.all().select_related('user', 'pet', 'pet__owner', 'pet__owner__profile')
    
    if not requests.exists():
        print("No adoption requests found in database.")
        return
    
    print(f"Total Adoption Requests: {requests.count()}")
    print("\nAdoption Request Details:")
    print("-" * 120)
    print(f"{'ID':<3} {'Requester':<15} {'Pet':<15} {'Status':<12} {'Shelter':<20} {'Reason':<30}")
    print("-" * 120)
    
    for req in requests:
        requester = req.user.username if req.user else "None"
        pet_name = req.pet.name if req.pet else "None"
        shelter_name = req.pet.owner.profile.shelter_name if req.pet and req.pet.owner and hasattr(req.pet.owner, 'profile') and req.pet.owner.profile.is_shelter else "-"
        reason = req.reason[:30] + "..." if len(req.reason) > 30 else req.reason
        
        print(f"{req.id:<3} {requester:<15} {pet_name:<15} {req.status:<12} {shelter_name:<20} {reason:<30}")

def check_chat_messages():
    print_separator("CHAT MESSAGES")
    messages = Message.objects.all().select_related('sender', 'receiver')
    
    if not messages.exists():
        print("No chat messages found in database.")
        return
    
    print(f"Total Chat Messages: {messages.count()}")
    print("\nChat Message Details:")
    print("-" * 100)
    print(f"{'ID':<3} {'Sender':<15} {'Receiver':<15} {'Content':<50} {'Date':<20}")
    print("-" * 100)
    
    for msg in messages:
        sender = msg.sender.username if msg.sender else "None"
        receiver = msg.receiver.username if msg.receiver else "None"
        content = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
        
        print(f"{msg.id:<3} {sender:<15} {receiver:<15} {content:<50} {msg.created_at.strftime('%Y-%m-%d %H:%M'):<20}")

def check_statistics():
    print_separator("DATABASE STATISTICS")
    
    # User statistics
    total_users = User.objects.count()
    shelter_users = UserProfile.objects.filter(is_shelter=True).count()
    regular_users = UserProfile.objects.filter(is_shelter=False).count()
    users_without_profile = User.objects.filter(profile__isnull=True).count()
    
    print(f"Users:")
    print(f"  Total Users: {total_users}")
    print(f"  Shelter Users: {shelter_users}")
    print(f"  Regular Users: {regular_users}")
    print(f"  Users without profile: {users_without_profile}")
    
    # Pet statistics
    total_pets = Pet.objects.count()
    available_pets = Pet.objects.filter(status='available').count()
    adopted_pets = Pet.objects.filter(status='adopted').count()
    pets_by_type = Pet.objects.values('pet_type').annotate(count=Count('id'))
    
    print(f"\nPets:")
    print(f"  Total Pets: {total_pets}")
    print(f"  Available Pets: {available_pets}")
    print(f"  Adopted Pets: {adopted_pets}")
    print(f"  Pets by Type:")
    for pet_type in pets_by_type:
        print(f"    {pet_type['pet_type']}: {pet_type['count']}")
    
    # Adoption request statistics
    total_requests = AdoptionRequest.objects.count()
    pending_requests = AdoptionRequest.objects.filter(status='pending').count()
    approved_requests = AdoptionRequest.objects.filter(status='approved').count()
    rejected_requests = AdoptionRequest.objects.filter(status='rejected').count()
    
    print(f"\nAdoption Requests:")
    print(f"  Total Requests: {total_requests}")
    print(f"  Pending: {pending_requests}")
    print(f"  Approved: {approved_requests}")
    print(f"  Rejected: {rejected_requests}")
    
    # Chat statistics
    total_messages = Message.objects.count()
    print(f"\nChat Messages:")
    print(f"  Total Messages: {total_messages}")

def main():
    print("🐾 Pet Adoption Platform - Database Status Check")
    print("=" * 60)
    
    try:
        check_users()
        check_pets()
        check_adoption_requests()
        check_chat_messages()
        check_statistics()
        
        print_separator("DATABASE CHECK COMPLETE")
        print("✅ Database is accessible and contains data!")
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    # Import Count for statistics
    from django.db.models import Count
    sys.exit(main()) 