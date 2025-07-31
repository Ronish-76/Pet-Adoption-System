from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import AdoptionRequest
from pets.models import Pet
from .serializers import (
    AdoptionRequestSerializer, AdoptionRequestUpdateSerializer,
    AdoptionRequestListSerializer, AdoptionStatisticsSerializer
)

@method_decorator(csrf_exempt, name='dispatch')
class AdoptionRequestListView(generics.ListCreateAPIView):
    """List and create adoption requests"""
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created']
    ordering = ['-created']

    def get_queryset(self):
        """Return user's own adoption requests"""
        return AdoptionRequest.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # The serializer already handles pet_id validation and conversion
        serializer.save(user=self.request.user)

@method_decorator(csrf_exempt, name='dispatch')
class AdoptionRequestDetailView(generics.RetrieveAPIView):
    """Get detailed information about an adoption request"""
    serializer_class = AdoptionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return user's own adoption requests"""
        return AdoptionRequest.objects.filter(user=self.request.user)

class AdminAdoptionRequestListView(generics.ListAPIView):
    """Admin view: List all adoption requests"""
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created']
    ordering = ['-created']

class AdminAdoptionRequestDetailView(generics.RetrieveUpdateAPIView):
    """Admin view: Get and update adoption request"""
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        # Only pet owner or shelter admin can update adoption requests
        if not (obj.pet.owner == self.request.user or 
                (hasattr(self.request.user, 'profile') and self.request.user.profile.is_shelter)):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to update this adoption request.")
        return obj

    def perform_update(self, serializer):
        adoption = self.get_object()
        new_status = self.request.data.get('status')
        
        with transaction.atomic():
            # Update adoption request status
            adoption = serializer.save()
            
            if new_status == 'approved':
                # Mark pet as adopted
                pet = adoption.pet
                pet.status = 'adopted'
                pet.save()
                
                # Reject all other pending requests for this pet
                AdoptionRequest.objects.filter(
                    pet=pet,
                    status='pending'
                ).exclude(id=adoption.id).update(status='rejected')
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': f'Adoption request {serializer.data["status"]} successfully',
            'adoption_request': AdoptionRequestSerializer(instance).data
        })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def adoption_statistics(request):
    """Get adoption statistics for admin dashboard"""
    total_requests = AdoptionRequest.objects.count()
    pending_requests = AdoptionRequest.objects.filter(status='pending').count()
    approved_requests = AdoptionRequest.objects.filter(status='approved').count()
    rejected_requests = AdoptionRequest.objects.filter(status='rejected').count()
    
    # Recent requests (last 10)
    recent_requests = AdoptionRequest.objects.select_related('user', 'pet').order_by('-created')[:10]
    recent_data = []
    for request in recent_requests:
        recent_data.append({
            'id': request.id,
            'user_name': request.user.get_full_name() or request.user.username,
            'pet_name': request.pet.name,
            'status': request.status,
            'created': request.created
        })
    
    data = {
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'recent_requests': recent_data
    }
    
    serializer = AdoptionStatisticsSerializer(data)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_update_adoptions(request):
    """Bulk update adoption request statuses (admin only)"""
    adoption_ids = request.data.get('adoption_ids', [])
    new_status = request.data.get('status')
    
    if not adoption_ids or not new_status:
        return Response({
            'error': 'Both adoption_ids and status are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if new_status not in ['approved', 'rejected']:
        return Response({
            'error': 'Status must be either "approved" or "rejected"'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update adoption requests
    updated_count = 0
    for adoption_id in adoption_ids:
        try:
            adoption = AdoptionRequest.objects.get(id=adoption_id)
            adoption.status = new_status
            adoption.save()
            
            # Update pet status if approved
            if new_status == 'approved':
                adoption.pet.status = 'adopted'
                adoption.pet.save()
            
            updated_count += 1
        except AdoptionRequest.DoesNotExist:
            continue
    
    return Response({
        'message': f'Successfully updated {updated_count} adoption requests',
        'updated_count': updated_count
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_adoption_history(request):
    """Get user's adoption history"""
    user_requests = AdoptionRequest.objects.filter(user=request.user).select_related('pet').order_by('-created')
    
    history = []
    for adoption in user_requests:
        history.append({
            'id': adoption.id,
            'pet_name': adoption.pet.name,
            'pet_type': adoption.pet.pet_type,
            'status': adoption.status,
            'reason': adoption.reason,
            'created': adoption.created
        })
    
    return Response({
        'adoption_history': history,
        'total_requests': len(history)
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def shelter_adoption_requests(request):
    """Get adoption requests for pets owned by the authenticated shelter"""
    # Check if user is a shelter
    if not hasattr(request.user, 'profile') or not request.user.profile.is_shelter:
        return Response({
            'error': 'Access denied. Only shelter accounts can view this endpoint.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Get adoption requests for pets owned by this shelter
    adoption_requests = AdoptionRequest.objects.filter(pet__owner=request.user).select_related('user', 'pet')
    serializer = AdoptionRequestListSerializer(adoption_requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_adoption_request(request, request_id):
    """Approve an adoption request (shelter only)"""
    # Check if user is a shelter
    if not hasattr(request.user, 'profile') or not request.user.profile.is_shelter:
        return Response({
            'error': 'Access denied. Only shelter accounts can approve adoption requests.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        adoption_request = AdoptionRequest.objects.get(id=request_id, pet__owner=request.user)
    except AdoptionRequest.DoesNotExist:
        return Response({
            'error': 'Adoption request not found or you do not have permission to approve it.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    with transaction.atomic():
        # Update adoption request status
        adoption_request.status = 'approved'
        adoption_request.save()
        
        # Mark pet as adopted
        pet = adoption_request.pet
        pet.status = 'adopted'
        pet.save()
        
        # Reject all other pending requests for this pet
        AdoptionRequest.objects.filter(
            pet=pet,
            status='pending'
        ).exclude(id=adoption_request.id).update(status='rejected')
    
    return Response({
        'message': 'Adoption request approved successfully',
        'adoption_request': AdoptionRequestSerializer(adoption_request).data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_adoption_request(request, request_id):
    """Reject an adoption request (shelter only)"""
    # Check if user is a shelter
    if not hasattr(request.user, 'profile') or not request.user.profile.is_shelter:
        return Response({
            'error': 'Access denied. Only shelter accounts can reject adoption requests.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        adoption_request = AdoptionRequest.objects.get(id=request_id, pet__owner=request.user)
    except AdoptionRequest.DoesNotExist:
        return Response({
            'error': 'Adoption request not found or you do not have permission to reject it.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    reason = request.data.get('reason', 'No reason provided')
    
    adoption_request.status = 'rejected'
    adoption_request.save()
    
    return Response({
        'message': 'Adoption request rejected successfully',
        'adoption_request': AdoptionRequestSerializer(adoption_request).data
    })

@method_decorator(csrf_exempt, name='dispatch')
class AdoptionRequestUpdateView(generics.UpdateAPIView):
    """Update adoption request status (shelter only)"""
    queryset = AdoptionRequest.objects.all()
    serializer_class = AdoptionRequestUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        # Only pet owner (shelter) can update adoption requests
        if obj.pet.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to update this adoption request.")
        return obj

    def perform_update(self, serializer):
        adoption = self.get_object()
        new_status = self.request.data.get('status')
        
        with transaction.atomic():
            # Update adoption request status
            adoption = serializer.save()
            
            if new_status == 'approved':
                # Mark pet as adopted
                pet = adoption.pet
                pet.status = 'adopted'
                pet.save()
                
                # Reject all other pending requests for this pet
                AdoptionRequest.objects.filter(
                    pet=pet,
                    status='pending'
                ).exclude(id=adoption.id).update(status='rejected')
            elif new_status == 'rejected' and adoption.pet.status == 'pending':
                # If rejecting and no other pending requests, make pet available again
                other_pending = AdoptionRequest.objects.filter(
                    pet=adoption.pet,
                    status='pending'
                ).exclude(id=adoption.id).exists()
                
                if not other_pending:
                    adoption.pet.status = 'available'
                    adoption.pet.save()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': f'Adoption request {serializer.data["status"]} successfully',
            'adoption_request': AdoptionRequestSerializer(instance).data
        })
