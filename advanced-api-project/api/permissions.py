from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For Author objects, check if the user is the owner
        # This is a placeholder - in a real app, you might want to check
        # against user attributes or a different ownership relationship
        return request.user.is_authenticated and request.user.is_staff