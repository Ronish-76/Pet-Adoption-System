from rest_framework import serializers
from .models import Pet
from django.contrib.auth.models import User

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for pet ownership"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class PetSerializer(serializers.ModelSerializer):
    """Main pet serializer"""
    owner = UserBasicSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'pet_type', 'breed', 'age', 'gender', 
            'description', 'status', 'image', 'image_url', 'owner',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

class PetCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating pets (admin only)"""
    class Meta:
        model = Pet
        fields = [
            'name', 'pet_type', 'breed', 'age', 'gender', 
            'description', 'status', 'image'
        ]

    def validate_image(self, image):
        if image:
            # Check file size (2MB limit)
            if image.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Image size cannot exceed 2MB.")
            
            # Check file type
            if not image.content_type.startswith('image/'):
                raise serializers.ValidationError("Only image files are allowed.")
            
            # Check specific formats
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if image.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG, PNG, and GIF images are allowed.")
        
        return image
    
    def validate_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Pet name must be at least 2 characters long.")
        return value.strip()
    
    def validate_age(self, value):
        if value < 0 or value > 30:
            raise serializers.ValidationError("Age must be between 0 and 30 years.")
        return value

    def create(self, validated_data):
        # Set the current user as the owner
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class PetUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating pets"""
    class Meta:
        model = Pet
        fields = [
            'name', 'pet_type', 'breed', 'age', 'gender', 
            'description', 'status', 'image'
        ]

class PetListSerializer(serializers.ModelSerializer):
    """Simplified serializer for pet listings"""
    image_url = serializers.SerializerMethodField()
    pet_type_display = serializers.CharField(source='get_pet_type_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'pet_type', 'pet_type_display', 'breed', 'age', 
            'gender', 'gender_display', 'status', 'image_url', 'created_at'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

class PetSearchSerializer(serializers.Serializer):
    """Serializer for pet search parameters"""
    search = serializers.CharField(required=False, help_text="Search in name, breed, or description")
    pet_type = serializers.ChoiceField(choices=Pet.PET_TYPES, required=False)
    gender = serializers.ChoiceField(choices=Pet.GENDER_CHOICES, required=False)
    status = serializers.ChoiceField(choices=Pet.STATUS_CHOICES, required=False)
    min_age = serializers.IntegerField(required=False, min_value=0)
    max_age = serializers.IntegerField(required=False, min_value=0)
    ordering = serializers.CharField(required=False, help_text="Order by: name, age, created_at") 