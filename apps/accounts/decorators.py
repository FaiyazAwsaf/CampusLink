from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


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


def cds_owner_required(view_func):
    """
    Decorator to require CDS Owner privileges
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)
        
        if request.user.role != 'cds_owner':
            return JsonResponse({
                'success': False,
                'error': 'CDS Owner privileges required'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper


# Keep admin_required for actual admin operations (superuser only)
def admin_required(view_func):
    """
    Decorator to require actual admin privileges (superuser only)
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


def laundry_staff_required(view_func):
    """
    Decorator to require Laundry Staff privileges
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
                'error': 'Laundry Staff privileges required'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper


# Keep staff_required for backward compatibility
staff_required = laundry_staff_required


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


def role_required(allowed_roles):
    """
    Decorator to check if user has one of the allowed roles
    allowed_roles: list of role names (e.g., ['laundry_staff', 'admin'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            if request.user.role not in allowed_roles:
                return JsonResponse({
                    'success': False,
                    'error': f'Access denied: Requires one of {allowed_roles} roles'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
