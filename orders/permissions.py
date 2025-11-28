from rest_framework import permissions


class IsOrderOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow order owners or admin to access orders.
    """
    
    def has_object_permission(self, request, view, obj):
        """Check if user is the order owner or admin."""
        # Admin has full access
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return True
        
        # Owner has access to their own orders
        return obj.customer == request.user
