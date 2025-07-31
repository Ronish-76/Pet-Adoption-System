from rest_framework import serializers
from .models import AdoptionRequest
from pets.models import Pet
from django.contrib.auth.models import User

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class PetBasicSerializer(serializers.ModelSerializer):
    """Basic pet serializer for adoption requests"""
    class Meta:
        model = Pet
        fields = ['id', 'name', 'pet_type', 'breed', 'age', 'image']

class AdoptionRequestSerializer(serializers.ModelSerializer):
    """Main adoption request serializer"""
    user = UserBasicSerializer(read_only=True)
    pet = PetBasicSerializer(read_only=True)
    pet_id = serializers.IntegerField(write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AdoptionRequest
        fields = [
            'id', 'user', 'pet', 'pet_id', 'reason', 'status', 
            'status_display', 'created'
        ]
        read_only_fields = ['id', 'user', 'status', 'created']

    def validate_pet_id(self, value):
        """Validate that the pet exists and is available"""
        if not value or value <= 0:
            raise serializers.ValidationError("Invalid pet ID.")
            
        try:
            pet = Pet.objects.get(id=value)
            if pet.status != 'available':
                raise serializers.ValidationError("This pet is not available for adoption.")
                
        except Pet.DoesNotExist:
            raise serializers.ValidationError("Pet not found.")
        
        return value
    
    def validate_reason(self, value):
        """Validate adoption reason"""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide a detailed reason (at least 10 characters).")
        if len(value) > 1000:
            raise serializers.ValidationError("Reason is too long (maximum 1000 characters).")
        return value.strip()

    def create(self, validated_data):
        from django.db import transaction
        
        pet_id = validated_data.pop('pet_id')
        
        with transaction.atomic():
            # Lock the pet to prevent race conditions
            pet = Pet.objects.select_for_update().get(id=pet_id)
            
            # Double-check availability after lock
            if pet.status != 'available':
                raise serializers.ValidationError("This pet is no longer available for adoption.")
            
            # Check for existing pending request
            user = self.context['request'].user
            if AdoptionRequest.objects.filter(user=user, pet=pet, status='pending').exists():
                raise serializers.ValidationError("You already have a pending request for this pet.")
            
            validated_data['pet'] = pet
            validated_data['user'] = user
            
            # Update pet status to pending
            pet.status = 'pending'
            pet.save()
            
            return super().create(validated_data)

class AdoptionRequestUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating adoption request status (admin only)"""
    class Meta:
        model = AdoptionRequest
        fields = ['status']

    def update(self, instance, validated_data):
        new_status = validated_data.get('status')
        
        # Update pet status when adoption is approved
        if new_status == 'approved':
            instance.pet.status = 'adopted'
            instance.pet.save()
        elif new_status == 'rejected' and instance.status == 'pending':
            # If rejecting a pending request, make pet available again
            if instance.pet.status == 'pending':
                instance.pet.status = 'available'
                instance.pet.save()
        
        return super().update(instance, validated_data)

class AdoptionRequestListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing adoption requests"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_type = serializers.CharField(source='pet.pet_type', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AdoptionRequest
        fields = [
            'id', 'user_name', 'pet_name', 'pet_type', 'status', 
            'status_display', 'created'
        ]

class AdoptionStatisticsSerializer(serializers.Serializer):
    """Serializer for adoption statistics"""
    total_requests = serializers.IntegerField()
    pending_requests = serializers.IntegerField()
    approved_requests = serializers.IntegerField()
    rejected_requests = serializers.IntegerField()
    recent_requests = serializers.ListField() 