from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from rest_framework.permissions import BasePermission

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_superuser or (request.user.role and request.user.role.name == role_name):
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied("You don't have permission to access this page")
        return wrapped
    return decorator

def permission_required(perm_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Check if user has permission directly or through role
                if (request.user.is_superuser or 
                    request.user.has_perm(perm_name) or 
                    (hasattr(request, 'role_permissions') and perm_name in request.role_permissions)):
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied("You don't have permission to access this page")
        return wrapped
    return decorator

# DRF Permission classes
class HasRolePermission(BasePermission):
    """
    Allows access only to users with the specified role.
    """
    def __init__(self, role_name):
        self.role_name = role_name
        
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_superuser or
             (request.user.role and request.user.role.name == self.role_name))
        )