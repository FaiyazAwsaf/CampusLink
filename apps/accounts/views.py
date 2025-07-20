from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
import json
import os

from .models import User, Roles
from .decorators import (
    login_required_json, 
    admin_required, 
    staff_required,
    role_required,
    cds_owner_required,
    laundry_staff_required,
    entrepreneur_required
)
from .permissions import PermissionManager, AuthorizationChecker
from .validators import ValidationUtils

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """
    Register a new user with the provided information
    """
    try:
        # Prepare data for validation
        registration_data = {
            'email': request.POST.get('email', ''),
            'name': request.POST.get('name', ''),
            'password': request.POST.get('password', ''),
            'phone': request.POST.get('phone', ''),
            'image': request.FILES.get('image')
        }
        
        # Validate all registration data
        try:
            validated_data = ValidationUtils.validate_registration_data(registration_data)
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'errors': e.message_dict if hasattr(e, 'message_dict') else {'general': str(e)}
            }, status=400)
        
        # Create user with validated data
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            phone=validated_data.get('phone'),
        )

        # Save image if provided
        if validated_data.get('image'):
            user.image = validated_data['image']
            user.save()

        # Assign user to appropriate group based on role
        if user.role == Roles.CDS_OWNER:
            PermissionManager.assign_user_to_group(user, 'CDS Owners')
        elif user.role == Roles.LAUNDRY_STAFF:
            PermissionManager.assign_user_to_group(user, 'Laundry Staff')
        elif user.role == Roles.ENTREPRENEUR:
            PermissionManager.assign_user_to_group(user, 'Entrepreneurs')
        else:  # student (default)
            PermissionManager.assign_user_to_group(user, 'Students')

        # Log the user in
        login(request, user)

        return JsonResponse({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                'role': user.role,
                'is_admin': user.is_admin,
                'is_verified': user.is_verified,
                'permissions': user.get_permissions_list(),
                'image': user.image.url if user.image else None
            }
        })

    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'errors': e.message_dict if hasattr(e, 'message_dict') else {'general': str(e)}
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """
    Log in a user with email and password
    """
    try:
        data = json.loads(request.body)
        
        # Validate login data
        try:
            validated_data = ValidationUtils.validate_login_data(data)
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'errors': e.message_dict if hasattr(e, 'message_dict') else {'general': str(e)}
            }, status=400)
        
        # Authenticate user
        user = authenticate(
            request, 
            email=validated_data['email'], 
            password=validated_data['password']
        )
        
        if user is None:
            return JsonResponse({
                'success': False,
                'error': 'Invalid email or password'
            }, status=401)
        
        # Check if user is active
        if not user.is_active:
            return JsonResponse({
                'success': False,
                'error': 'Account is inactive. Please contact support.'
            }, status=403)
        
        # Log the user in
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                'role': user.role,
                'is_admin': user.is_admin,
                'is_verified': user.is_verified,
                'permissions': user.get_permissions_list(),
                'image': user.image.url if user.image else None
            }
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Login failed: {str(e)}'
        }, status=500)

@require_http_methods(["POST"])
def logout_user(request):
    """
    Log out the current user
    """
    try:
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_current_user(request):
    """
    Get the current logged-in user's information
    """
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                'role': user.role,
                'is_admin': user.is_admin,
                'is_verified': user.is_verified,
                'permissions': user.get_permissions_list(),
                'image': user.image.url if user.image else None
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated'
        }, status=401)


# Authorization-related views

@login_required_json
@require_http_methods(["GET"])
def check_permission(request):
    """
    Check if current user has specific permission
    """
    permission = request.GET.get('permission')
    if not permission:
        return JsonResponse({
            'success': False,
            'error': 'Permission parameter required'
        }, status=400)
    
    has_permission = request.user.has_perm(permission)
    
    return JsonResponse({
        'success': True,
        'has_permission': has_permission,
        'permission': permission
    })


@login_required_json
@require_http_methods(["GET"])
def get_user_role(request):
    """
    Get current user's role and permissions for frontend
    """
    try:
        user = request.user
        
        return JsonResponse({
            'success': True,
            'user_role': {
                'role': user.role,
                'role_display': user.get_role_display(),
                'permissions': user.get_permissions_list(),
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'can_manage_users': user.is_superuser,
                'can_access_admin': user.role in [Roles.CDS_OWNER, Roles.LAUNDRY_STAFF] or user.is_superuser
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required_json
@require_http_methods(["GET"])
def get_user_permissions(request):
    """
    Get all permissions for current user
    """
    permissions = request.user.get_permissions_list()
    
    return JsonResponse({
        'success': True,
        'permissions': permissions
    })


@admin_required
@require_http_methods(["GET"])
def list_users(request):
    """
    List all users (superuser only)
    """
    users = User.objects.all().values(
        'id', 'email', 'name', 'phone', 'role', 
        'is_admin', 'is_verified', 'is_active', 'created_at'
    )
    
    return JsonResponse({
        'success': True,
        'users': list(users)
    })


@admin_required
@require_http_methods(["POST"])
def change_user_role(request):
    """
    Change user role (superuser only)
    """
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        new_role = data.get('role')
        
        if not all([user_id, new_role]):
            return JsonResponse({
                'success': False,
                'error': 'user_id and role are required'
            }, status=400)
        
        # Validate role
        valid_roles = [choice[0] for choice in Roles.CHOICES]
        if new_role not in valid_roles:
            return JsonResponse({
                'success': False,
                'error': f'Invalid role. Must be one of: {valid_roles}'
            }, status=400)
        
        user = User.objects.get(id=user_id)
        old_role = user.role
        user.role = new_role
        user.save()
        
        # Update user groups
        user.groups.clear()  # Remove from all groups
        
        if new_role == Roles.CDS_OWNER:
            PermissionManager.assign_user_to_group(user, 'CDS Owners')
        elif new_role == Roles.LAUNDRY_STAFF:
            PermissionManager.assign_user_to_group(user, 'Laundry Staff')
        elif new_role == Roles.ENTREPRENEUR:
            PermissionManager.assign_user_to_group(user, 'Entrepreneurs')
        else:  # student
            PermissionManager.assign_user_to_group(user, 'Students')
        
        return JsonResponse({
            'success': True,
            'message': f'User role changed from {old_role} to {new_role}',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'permissions': user.get_permissions_list()
            }
        })
    
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@admin_required
@require_http_methods(["POST"])
def toggle_user_status(request):
    """
    Toggle user active/inactive status (superuser only)
    """
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        if not user_id:
            return JsonResponse({
                'success': False,
                'error': 'user_id is required'
            }, status=400)
        
        user = User.objects.get(id=user_id)
        
        # Don't allow admin to deactivate themselves
        if user == request.user:
            return JsonResponse({
                'success': False,
                'error': 'Cannot change your own status'
            }, status=400)
        
        user.is_active = not user.is_active
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': f'User {"activated" if user.is_active else "deactivated"}',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'is_active': user.is_active
            }
        })
    
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required_json
@require_http_methods(["POST"])
def update_profile(request):
    """
    Update user profile (users can only update their own profile, unless superuser)
    """
    try:
        target_user_id = request.POST.get('user_id')
        
        # If no user_id provided, update own profile
        if not target_user_id:
            target_user = request.user
        else:
            # Only superusers can update other users' profiles
            if not request.user.is_superuser:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied: You can only update your own profile'
                }, status=403)
            
            try:
                target_user = User.objects.get(id=target_user_id)
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'User not found'
                }, status=404)
        
        # Prepare update data for validation
        update_data = {}
        
        # Only allow updating specific fields
        allowed_fields = ['name', 'phone']
        
        for field in allowed_fields:
            if field in request.POST:
                update_data[field] = request.POST.get(field)
        
        # Handle image separately
        if 'image' in request.FILES:
            update_data['image'] = request.FILES.get('image')
        
        # Validate the update data
        try:
            validated_data = ValidationUtils.validate_profile_update_data(update_data, target_user)
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'errors': e.message_dict if hasattr(e, 'message_dict') else {'general': str(e)}
            }, status=400)
        
        # Update the user with validated data
        for field, value in validated_data.items():
            if field != 'image':  # Handle image separately
                setattr(target_user, field, value)
        
        # Handle image update
        if 'image' in validated_data:
            target_user.image = validated_data['image']
        
        target_user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'id': target_user.id,
                'email': target_user.email,
                'name': target_user.name,
                'phone': target_user.phone,
                'role': target_user.role,
                'image': target_user.image.url if target_user.image else None
            }
        })
    
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required_json
@require_http_methods(["GET"])
def get_user_profile(request, user_id=None):
    """
    Get user profile (own profile or any profile if superuser)
    """
    try:
        # If no user_id provided, get own profile
        if not user_id:
            target_user = request.user
        else:
            # Only superusers can view other users' profiles
            if not request.user.is_superuser:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied: You can only view your own profile'
                }, status=403)
            
            try:
                target_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'User not found'
                }, status=404)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': target_user.id,
                'email': target_user.email,
                'name': target_user.name,
                'phone': target_user.phone,
                'role': target_user.role,
                'is_verified': target_user.is_verified,
                'is_active': target_user.is_active,
                'created_at': target_user.created_at.isoformat() if target_user.created_at else None,
                'image': target_user.image.url if target_user.image else None
            }
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
