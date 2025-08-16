from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .validators import ValidationUtils


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    name = serializers.CharField(max_length=255, required=True)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'name', 'phone', 'image']

    def validate(self, attrs):
        """
        Custom validation for registration data
        """
        # Check password confirmation
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })

        # Use existing validation utils
        try:
            ValidationUtils.validate_registration_data({
                'email': attrs.get('email'),
                'name': attrs.get('name'),
                'password': attrs.get('password'),
                'phone': attrs.get('phone'),
                'image': attrs.get('image')
            })
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs

    def create(self, validated_data):
        """
        Create a new user with validated data
        """
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop('password_confirm', None)
        
        # Create user
        user = User.objects.create_user(**validated_data)
        
        # Assign to default group
        from .permissions import PermissionManager
        PermissionManager.assign_user_to_group(user, 'Students')
        
        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Custom JWT token serializer that uses email instead of username
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Custom validation for login
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({
                'detail': 'Email and password are required'
            })

        # Use Django's authenticate
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError({
                'detail': 'Invalid email or password'
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'detail': 'Account is inactive. Please contact support.'
            })

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Add custom claims to the refresh token
        refresh['email'] = user.email
        refresh['name'] = user.name
        refresh['role'] = user.role
        refresh['is_admin'] = user.is_admin
        refresh['is_verified'] = user.is_verified
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserProfileSerializer(user, context=self.context).data
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data
    """
    permissions = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'phone', 'role', 
            'is_admin', 'is_verified', 'is_active', 
            'created_at', 'permissions', 'image_url'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_admin', 'created_at']

    def get_permissions(self, obj):
        """Get user permissions list"""
        return obj.get_permissions_list()

    def get_image_url(self, obj):
        """Get absolute URL for user image"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def update(self, instance, validated_data):
        """
        Update user profile with validation
        """
        # Only allow certain fields to be updated
        allowed_fields = ['name', 'phone', 'image']
        
        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        
        # Validate the updated instance
        instance.full_clean()
        instance.save()
        
        return instance


class TokenRefreshResponseSerializer(serializers.Serializer):
    """
    Serializer for token refresh response
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserProfileSerializer(read_only=True)


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout (token blacklisting)
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception:
            # Token is already blacklisted or invalid
            pass


class ChangeRoleSerializer(serializers.Serializer):
    """
    Serializer for changing user roles (CDS Owner only)
    """
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

    def save(self):
        user_id = self.validated_data['user_id']
        new_role = self.validated_data['role']
        
        user = User.objects.get(id=user_id)
        old_role = user.role
        user.role = new_role
        user.save()

        # Update user groups
        from .permissions import PermissionManager
        user.groups.clear()
        
        role_group_mapping = {
            'cds_owner': 'CDS Owners',
            'staff': 'Staff',
            'entrepreneur': 'Entrepreneurs',
            'student': 'Students'
        }
        
        group_name = role_group_mapping.get(new_role, 'Students')
        PermissionManager.assign_user_to_group(user, group_name)
        
        return user, old_role


class ToggleUserStatusSerializer(serializers.Serializer):
    """
    Serializer for toggling user active status (CDS Owner only)
    """
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

    def save(self, current_user):
        user_id = self.validated_data['user_id']
        user = User.objects.get(id=user_id)
        
        # Don't allow CDS Owner to deactivate themselves
        if user == current_user:
            raise serializers.ValidationError("Cannot change your own status")
        
        user.is_active = not user.is_active
        user.save()
        
        return user
