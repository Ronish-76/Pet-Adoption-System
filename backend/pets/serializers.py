from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pet, AdoptionRequest, Shelter, Favorite, Notification, PetMedicalInfo

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class AdoptionRequestSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    
    class Meta:
        model = AdoptionRequest
        fields = '__all__'

class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    
    class Meta:
        model = Favorite
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class PetMedicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetMedicalInfo
        fields = '__all__'