from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Pet, AdoptionRequest, Shelter, Favorite, Notification, PetMedicalInfo
from .serializers import PetSerializer, AdoptionRequestSerializer, FavoriteSerializer, NotificationSerializer

@api_view(['GET'])
def get_pets(request):
    try:
        pets = Pet.objects.filter(deleted_at__isnull=True)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_pet(request):
    serializer = PetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_adoptions(request):
    adoptions = AdoptionRequest.objects.all()
    serializer = AdoptionRequestSerializer(adoptions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@transaction.atomic
def create_adoption(request):
    pet_id = request.data.get('pet')
    user_id = request.data.get('user')
    
    try:
        pet = Pet.objects.select_for_update().get(id=pet_id)
        
        # Check if pet is still available
        if pet.status != 'available':
            return Response({'error': 'Pet is no longer available for adoption'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for existing pending request from same user
        existing_request = AdoptionRequest.objects.filter(
            pet_id=pet_id, 
            user_id=user_id, 
            status='pending'
        ).first()
        
        if existing_request:
            return Response({'error': 'You already have a pending request for this pet'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create adoption request
        adoption_request = AdoptionRequest.objects.create(
            pet_id=pet_id,
            user_id=user_id,
            status='pending'
        )
        
        serializer = AdoptionRequestSerializer(adoption_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Pet.DoesNotExist:
        return Response({'error': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@transaction.atomic
def update_adoption(request, adoption_id):
    try:
        adoption = AdoptionRequest.objects.select_for_update().get(id=adoption_id)
        new_status = request.data.get('status', adoption.status)
        
        if new_status == 'approved':
            # Double-check pet is still available
            pet = Pet.objects.select_for_update().get(id=adoption.pet.id)
            if pet.status != 'available':
                return Response({'error': 'Pet is no longer available'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Approve this request
            adoption.status = 'approved'
            adoption.response_date = timezone.now()
            adoption.save()
            
            # Update pet status to adopted
            pet.status = 'adopted'
            pet.save()
            
            # Reject all other pending requests for this pet
            other_requests = AdoptionRequest.objects.filter(
                pet=pet,
                status='pending'
            ).exclude(id=adoption_id)
            
            for other_request in other_requests:
                other_request.status = 'rejected'
                other_request.response_date = timezone.now()
                other_request.notes = 'Pet was adopted by another user'
                other_request.save()
                
                # Notify rejected users
                if other_request.user:
                    Notification.objects.create(
                        user=other_request.user,
                        title='Adoption Request Update',
                        message=f'Unfortunately, {pet.name} has been adopted by another user. Please browse other available pets.'
                    )
            
            # Notify approved user
            if adoption.user:
                Notification.objects.create(
                    user=adoption.user,
                    title='Adoption Approved!',
                    message=f'Congratulations! Your adoption request for {pet.name} has been approved!'
                )
        
        elif new_status == 'rejected':
            adoption.status = 'rejected'
            adoption.response_date = timezone.now()
            adoption.notes = request.data.get('notes', '')
            adoption.save()
            
            # Notify rejected user
            if adoption.user:
                Notification.objects.create(
                    user=adoption.user,
                    title='Adoption Request Update',
                    message=f'Your adoption request for {adoption.pet.name} has been reviewed. Please check your adoption history for details.'
                )
        
        serializer = AdoptionRequestSerializer(adoption)
        return Response(serializer.data)
        
    except AdoptionRequest.DoesNotExist:
        return Response({'error': 'Adoption request not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_pets_filtered(request):
    # Only show available pets that haven't been soft deleted
    pets = Pet.objects.filter(
        status='available', 
        deleted_at__isnull=True
    ).select_related('shelter')
    
    # Apply filters
    pet_type = request.GET.get('type')
    if pet_type:
        pets = pets.filter(pet_type=pet_type)
    
    age_filter = request.GET.get('age')
    if age_filter == 'young':
        pets = pets.filter(age__lte=2)
    elif age_filter == 'adult':
        pets = pets.filter(age__gt=2, age__lte=7)
    elif age_filter == 'senior':
        pets = pets.filter(age__gt=7)
    
    serializer = PetSerializer(pets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def check_pet_availability(request, pet_id):
    """Check if a pet is still available before user submits adoption request"""
    try:
        pet = Pet.objects.get(id=pet_id)
        is_available = pet.status == 'available' and pet.deleted_at is None
        
        # Check if user already has pending request
        user_id = request.GET.get('user_id')
        has_pending = False
        if user_id:
            has_pending = AdoptionRequest.objects.filter(
                pet_id=pet_id,
                user_id=user_id,
                status='pending'
            ).exists()
        
        return Response({
            'available': is_available,
            'status': pet.status,
            'has_pending_request': has_pending
        })
    except Pet.DoesNotExist:
        return Response({'error': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_favorite(request):
    user_id = request.data.get('user_id')
    pet_id = request.data.get('pet_id')
    
    # Check if pet exists and is available
    try:
        pet = Pet.objects.get(id=pet_id, deleted_at__isnull=True)
    except Pet.DoesNotExist:
        return Response({'error': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)
    
    favorite, created = Favorite.objects.get_or_create(
        user_id=user_id,
        pet_id=pet_id
    )
    
    if created:
        return Response({'message': 'Pet added to favorites'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Pet already in favorites'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user_notifications(request, user_id):
    notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'is_read': n.is_read,
        'created_at': n.created_at
    } for n in notifications]
    return Response(data)

@api_view(['GET'])
def get_pet_detail(request, pet_id):
    """Get detailed information about a specific pet"""
    try:
        pet = Pet.objects.get(id=pet_id, deleted_at__isnull=True)
        serializer = PetSerializer(pet)
        return Response(serializer.data)
    except Pet.DoesNotExist:
        return Response({'error': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_featured_pets(request):
    """Get featured pets for homepage"""
    try:
        featured_pets = Pet.objects.filter(
            status='available',
            deleted_at__isnull=True
        ).order_by('-created_at')[:6]
        serializer = PetSerializer(featured_pets, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)