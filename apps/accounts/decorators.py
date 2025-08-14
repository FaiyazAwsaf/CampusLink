from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


def login_required_json(view_func):
    """
    Decorator to require authentication for JSON API endpoints
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Decorator to require admin privileges
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        
        if not request.user.is_admin:
            return JsonResponse({
                'success': False,
                'error': 'Admin privileges required'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_required(view_func):
    """
    Decorator to require staff privileges
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        
        if not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'Staff privileges required'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def superuser_required(view_func):
    """
    Decorator to require superuser privileges
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        
        if not request.user.is_superuser:
            return JsonResponse({
                'success': False,
                'error': 'Superuser privileges required'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def user_owns_resource(get_resource_user):
    """
    Decorator to check if user owns a resource
    get_resource_user: function that takes request and returns the user who owns the resource
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            resource_user = get_resource_user(request, *args, **kwargs)
            
            if request.user != resource_user and not request.user.is_admin:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied: You can only access your own resources'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def permission_required(permission_name):
    """
    Decorator to check if user has specific permission
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            if not request.user.has_perm(permission_name):
                return JsonResponse({
                    'success': False,
                    'error': f'Permission denied: {permission_name} required'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# JWT-compatible decorators for DRF views
def admin_required_jwt(view_func):
    """
    Decorator to require admin privileges for DRF views
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.is_admin:
            return Response({
                'success': False,
                'error': 'Admin privileges required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_required_jwt(view_func):
    """
    Decorator to require staff privileges for DRF views
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.is_staff:
            return Response({
                'success': False,
                'error': 'Staff privileges required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def permission_required_jwt(permission_name):
    """
    Decorator to check if user has specific permission for DRF views
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response({
                    'success': False,
                    'error': 'Authentication required'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            if not request.user.has_perm(permission_name):
                return Response({
                    'success': False,
                    'error': f'Permission denied: {permission_name} required'
                }, status=status.HTTP_403_FORBIDDEN)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
