from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    LogoutSerializer,
    ChangeRoleSerializer,
    ToggleUserStatusSerializer,
    TokenRefreshResponseSerializer
)
from .decorators import admin_required
from .permissions import PermissionManager


@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login(request):
    """
    Custom JWT login view
    """
    try:
        serializer = CustomTokenObtainPairSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({
                'success': True,
                'message': 'Login successful',
                'tokens': {
                    'access': serializer.validated_data['access'],
                    'refresh': serializer.validated_data['refresh']
                },
                'user': serializer.validated_data['user']
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom JWT token refresh view
    """
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            # Get user from refresh token
            refresh_token = request.data.get('refresh')
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    user_id = token.payload.get('user_id')
                    user = User.objects.get(id=user_id)
                    
                    return Response({
                        'success': True,
                        'tokens': response.data,
                        'user': UserProfileSerializer(user, context={'request': request}).data
                    }, status=status.HTTP_200_OK)
                except Exception:
                    pass
            
            return Response({
                'success': True,
                'tokens': response.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': 'Token refresh failed'
            }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and return JWT tokens
    """
    try:
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': 'User registered successfully',
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                },
                'user': UserProfileSerializer(user, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Registration failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by blacklisting refresh token
    """
    try:
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception:
        return Response({
            'success': True,
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get current authenticated user's information
    """
    try:
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response({
            'success': True,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update user profile
    """
    try:
        target_user_id = request.data.get('user_id')
        
        # If no user_id provided, update own profile
        if not target_user_id:
            target_user = request.user
        else:
            try:
                target_user = User.objects.get(id=target_user_id)
                # Check if user can modify this profile
                if not request.user.can_modify_user_data(target_user):
                    return Response({
                        'success': False,
                        'error': 'Permission denied'
                    }, status=status.HTTP_403_FORBIDDEN)
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(
            target_user, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_permission(request):
    """
    Check if current user has specific permission
    """
    permission = request.GET.get('permission')
    if not permission:
        return Response({
            'success': False,
            'error': 'Permission parameter required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    has_permission = request.user.has_perm(permission)
    
    return Response({
        'success': True,
        'has_permission': has_permission,
        'permission': permission
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_permissions(request):
    """
    Get all permissions for current user
    """
    permissions = request.user.get_permissions_list()
    
    return Response({
        'success': True,
        'permissions': permissions
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@admin_required
def list_users(request):
    """
    List all users (Admin only - for system administration)
    """
    try:
        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'users': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@admin_required
def change_user_role(request):
    """
    Change user role (Admin only - for system administration)
    """
    try:
        serializer = ChangeRoleSerializer(data=request.data)
        if serializer.is_valid():
            user, old_role = serializer.save()
            
            return Response({
                'success': True,
                'message': f'User role changed from {old_role} to {user.role}',
                'user': UserProfileSerializer(user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@admin_required
def toggle_user_status(request):
    """
    Toggle user active/inactive status (Admin only - for system administration)
    """
    try:
        serializer = ToggleUserStatusSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(current_user=request.user)
            
            return Response({
                'success': True,
                'message': f'User {"activated" if user.is_active else "deactivated"}',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'is_active': user.is_active
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    CSRF token endpoint (for backward compatibility)
    """
    return Response({
        'success': True, 
        'message': 'CSRF not required for JWT authentication'
    }, status=status.HTTP_200_OK)
