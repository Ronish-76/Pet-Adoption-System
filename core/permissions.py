from rest_framework.permissions import BasePermission

class IsShelterAdmin(BasePermission):
    """Permission for shelter administrators"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and
            request.user.profile.is_shelter
        )

class IsOwnerOrReadOnly(BasePermission):
    """Permission to only allow owners to edit their objects"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions only to owner
        return obj.owner == request.user

class IsPetOwner(BasePermission):
    """Permission for pet owners"""
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user