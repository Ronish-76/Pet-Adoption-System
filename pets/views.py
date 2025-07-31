from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Pet
from .serializers import (
    PetSerializer, PetCreateSerializer, PetUpdateSerializer, 
    PetListSerializer, PetSearchSerializer
)

class PetListView(generics.ListAPIView):
    """List all pets with search and filtering"""
    queryset = Pet.objects.all()
    serializer_class = PetListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pet_type', 'gender', 'status']
    search_fields = ['name', 'breed', 'description']
    ordering_fields = ['name', 'age', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Only show available pets by default
        queryset = Pet.objects.filter(status='available')
        
        # Custom filtering
        min_age = self.request.query_params.get('min_age')
        max_age = self.request.query_params.get('max_age')
        
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        if max_age:
            queryset = queryset.filter(age__lte=max_age)
            
        return queryset

class PetDetailView(generics.RetrieveAPIView):
    """Get detailed information about a specific pet"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.AllowAny]

class PetCreateView(generics.CreateAPIView):
    """Create a new pet (shelter admin only)"""
    queryset = Pet.objects.all()
    serializer_class = PetCreateSerializer
    
    def get_permissions(self):
        from core.permissions import IsShelterAdmin
        return [IsShelterAdmin()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PetUpdateView(generics.UpdateAPIView):
    """Update pet information (owner only)"""
    queryset = Pet.objects.all()
    serializer_class = PetUpdateSerializer
    
    def get_permissions(self):
        from core.permissions import IsPetOwner
        return [IsPetOwner()]

class PetDeleteView(generics.DestroyAPIView):
    """Delete a pet (admin only)"""
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Pet deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_pets(request):
    """Get featured pets for homepage"""
    featured = Pet.objects.filter(status='available').order_by('-created_at')[:6]
    serializer = PetListSerializer(featured, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def pet_statistics(request):
    """Get pet statistics for admin dashboard"""
    total_pets = Pet.objects.count()
    available_pets = Pet.objects.filter(status='available').count()
    adopted_pets = Pet.objects.filter(status='adopted').count()
    pending_pets = Pet.objects.filter(status='pending').count()
    
    # Pet type distribution
    pet_types = {}
    for pet_type, _ in Pet.PET_TYPES:
        pet_types[pet_type] = Pet.objects.filter(pet_type=pet_type).count()
    
    return Response({
        'total_pets': total_pets,
        'available_pets': available_pets,
        'adopted_pets': adopted_pets,
        'pending_pets': pending_pets,
        'pet_types': pet_types
    })

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def search_pets(request):
    """Advanced pet search"""
    serializer = PetSearchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    queryset = Pet.objects.all()
    
    # Search in name, breed, or description
    search = serializer.validated_data.get('search')
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(breed__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Filter by pet type
    pet_type = serializer.validated_data.get('pet_type')
    if pet_type:
        queryset = queryset.filter(pet_type=pet_type)
    
    # Filter by gender
    gender = serializer.validated_data.get('gender')
    if gender:
        queryset = queryset.filter(gender=gender)
    
    # Filter by status
    status_filter = serializer.validated_data.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    # Filter by age range
    min_age = serializer.validated_data.get('min_age')
    max_age = serializer.validated_data.get('max_age')
    
    if min_age is not None:
        queryset = queryset.filter(age__gte=min_age)
    if max_age is not None:
        queryset = queryset.filter(age__lte=max_age)
    
    # Ordering
    ordering = serializer.validated_data.get('ordering')
    if ordering:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by('-created_at')
    
    serializer_result = PetListSerializer(queryset, many=True, context={'request': request})
    return Response(serializer_result.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def shelter_pets(request):
    """Get pets owned by the authenticated shelter"""
    from core.permissions import IsShelterAdmin
    
    # Check if user is a shelter
    if not hasattr(request.user, 'profile') or not request.user.profile.is_shelter:
        return Response({
            'error': 'Access denied. Only shelter accounts can view this endpoint.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Get pets owned by this shelter
    pets = Pet.objects.filter(owner=request.user)
    serializer = PetListSerializer(pets, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def shelter_adoption_requests(request):
    """Get adoption requests for pets owned by the authenticated shelter"""
    from core.permissions import IsShelterAdmin
    
    # Check if user is a shelter
    if not hasattr(request.user, 'profile') or not request.user.profile.is_shelter:
        return Response({
            'error': 'Access denied. Only shelter accounts can view this endpoint.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Get adoption requests for pets owned by this shelter
    from adoption.models import AdoptionRequest
    adoption_requests = AdoptionRequest.objects.filter(pet__owner=request.user)
    
    from adoption.serializers import AdoptionRequestSerializer
    serializer = AdoptionRequestSerializer(adoption_requests, many=True)
    return Response(serializer.data)
