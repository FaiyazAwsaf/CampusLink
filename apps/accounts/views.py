from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os

from .models import User

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """
    Register a new user with the provided information
    """
    try:
        # For multipart/form-data: use request.POST (text) and request.FILES (file)
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')  # This is the uploaded image file

        # Validate required fields
        if not all([email, name, password]):
            return JsonResponse({
                'success': False,
                'error': 'Email, name, and password are required'
            }, status=400)

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'User with this email already exists'
            }, status=400)

        # Create user
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password,
            phone=phone
        )

        # Save image if provided
        if image:
            user.image = image
            user.save()

        # Log the user in
        login(request, user)

        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                'is_admin': user.is_admin,
                'image': user.image.url if user.image else None
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """
    Log in a user with email and password
    """
    try:
        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return JsonResponse({
                'success': False,
                'error': 'Email and password are required'
            }, status=400)
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return JsonResponse({
                'success': False,
                'error': 'Invalid email or password'
            }, status=401)
        
        # Log the user in
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                'is_admin': user.is_admin,
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
            'error': str(e)
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
                'is_admin': user.is_admin,
                'image': user.image.url if user.image else None
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Not authenticated'
        }, status=401)
