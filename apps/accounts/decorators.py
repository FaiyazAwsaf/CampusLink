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


def admin_required(view_func):
    """
    Decorator to require superuser privileges (since admin role was removed)
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


def role_required(required_role):
    """
    Decorator to require specific role
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'success': False,
                    'error': 'Authentication required'
                }, status=401)
            
            if not request.user.has_role(required_role):
                return JsonResponse({
                    'success': False,
                    'error': f'Permission denied: {required_role} role required'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def cds_owner_required(view_func):
    """
    Decorator to require CDS owner role
    """
    from .models import Roles
    return role_required(Roles.CDS_OWNER)(view_func)


def laundry_staff_required(view_func):
    """
    Decorator to require laundry staff role
    """
    from .models import Roles
    return role_required(Roles.LAUNDRY_STAFF)(view_func)


def entrepreneur_required(view_func):
    """
    Decorator to require entrepreneur role
    """
    from .models import Roles
    return role_required(Roles.ENTREPRENEUR)(view_func)
