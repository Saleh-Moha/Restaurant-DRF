from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read-only access is allowed for unauthenticated users.
    """

    def has_permission(self, request, view):
        # Allow read-only access for any request (both authenticated and unauthenticated users)
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed for authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any request
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed for the owner of the object
        return obj.id == request.user.id
