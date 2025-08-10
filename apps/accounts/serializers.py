from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer that includes user data in response"""
    
    def validate(self, attrs):
        # Get the default validated data
        data = super().validate(attrs)
        
        # Add user data to the response
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'phone': user.phone,
            'is_verified': user.is_verified,
            'is_superuser': user.is_superuser,
            'image': user.image.url if user.image else None,
            'permissions': user.get_permissions_list(),
        }
        
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims to the token
        token['user_id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        token['name'] = user.name
        token['is_superuser'] = user.is_superuser
        
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """Custom token refresh serializer that includes user data"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Get user from the refresh token
        refresh_token = RefreshToken(attrs['refresh'])
        user_id = refresh_token.payload.get('user_id')
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                data['user'] = {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'role': user.role,
                    'phone': user.phone,
                    'is_verified': user.is_verified,
                    'is_superuser': user.is_superuser,
                    'image': user.image.url if user.image else None,
                    'permissions': user.get_permissions_list(),
                }
            except User.DoesNotExist:
                pass
        
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'password', 'confirm_password', 'image')
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'phone', 'role', 'is_verified', 
                 'is_superuser', 'image', 'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'role', 'is_verified', 'is_superuser', 
                           'created_at', 'updated_at')


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
