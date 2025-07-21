from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import json

from .models import User, Roles
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    UserRegistrationSerializer,
    UserProfileSerializer,
    PasswordChangeSerializer
)
from .validators import ValidationUtils


class LoginView(TokenObtainPairView):
    """JWT-based login view"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class TokenRefreshView(TokenRefreshView):
    """JWT token refresh view"""
    serializer_class = CustomTokenRefreshSerializer


class RegisterView(generics.CreateAPIView):
    """User registration view with JWT token generation"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            # Validate registration data
            registration_data = {
                'email': request.data.get('email', ''),
                'name': request.data.get('name', ''),
                'password': request.data.get('password', ''),
                'confirm_password': request.data.get('confirm_password', ''),
                'phone': request.data.get('phone', ''),
                'image': request.FILES.get('image')
            }
            
            # Use existing validation utils
            try:
                validated_data = ValidationUtils.validate_registration_data({
                    'email': registration_data['email'],
                    'name': registration_data['name'],
                    'password': registration_data['password'],
                    'phone': registration_data['phone'],
                    'image': registration_data['image']
                })
            except ValidationError as e:
                return Response({
                    'success': False,
                    'errors': e.message_dict if hasattr(e, 'message_dict') else {'general': str(e)}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check password confirmation
            if registration_data['password'] != registration_data['confirm_password']:
                return Response({
                    'success': False,
                    'errors': {'confirm_password': ['Passwords do not match']}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create user
            serializer = self.get_serializer(data=registration_data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                
                # Add custom claims
                access_token['user_id'] = user.id
                access_token['email'] = user.email
                access_token['role'] = user.role
                access_token['name'] = user.name
                access_token['is_superuser'] = user.is_superuser
                
                return Response({
                    'success': True,
                    'message': 'User registered successfully',
                    'access': str(access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'name': user.name,
                        'phone': user.phone,
                        'role': user.role,
                        'is_verified': user.is_verified,
                        'is_superuser': user.is_superuser,
                        'image': user.image.url if user.image else None,
                        'permissions': user.get_permissions_list(),
                    }
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': 'Registration failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout view that blacklists the refresh token"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'success': True,
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
    
    except TokenError:
        return Response({
            'success': False,
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Logout failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current authenticated user"""
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response({
        'success': True,
        'user': serializer.data
    })


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Update user profile"""
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Change user password"""
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'success': True,
            'message': 'Password changed successfully'
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token_view(request):
    """Verify if the current JWT token is valid"""
    return Response({
        'success': True,
        'valid': True,
        'user': {
            'id': request.user.id,
            'email': request.user.email,
            'role': request.user.role
        }
    })
