from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.utils import timezone
import jwt
from django.conf import settings

User = get_user_model()


class JWTManager:
    """Utility class for JWT token management"""
    
    @staticmethod
    def generate_tokens_for_user(user):
        """Generate access and refresh tokens for a user"""
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        # Add custom claims
        access['user_id'] = user.id
        access['email'] = user.email
        access['role'] = user.role
        access['name'] = user.name
        access['is_superuser'] = user.is_superuser
        
        return {
            'access': str(access),
            'refresh': str(refresh)
        }
    
    @staticmethod
    def validate_token(token_string):
        """Validate a JWT token and return the user"""
        try:
            token = AccessToken(token_string)
            user_id = token.payload.get('user_id')
            
            if user_id:
                user = User.objects.get(id=user_id)
                if user.is_active:
                    return user
            return None
        except (TokenError, User.DoesNotExist):
            return None
    
    @staticmethod
    def decode_token(token_string):
        """Decode a JWT token and return its payload"""
        try:
            payload = jwt.decode(
                token_string, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            return payload
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def is_token_expired(token_string):
        """Check if a token is expired"""
        try:
            payload = JWTManager.decode_token(token_string)
            if payload:
                exp_timestamp = payload.get('exp')
                if exp_timestamp:
                    exp_datetime = timezone.datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
                    return timezone.now() >= exp_datetime
            return True
        except Exception:
            return True
    
    @staticmethod
    def refresh_token(refresh_token_string):
        """Refresh an access token using a refresh token"""
        try:
            refresh_token = RefreshToken(refresh_token_string)
            new_access_token = refresh_token.access_token
            
            # Get user and add custom claims
            user_id = refresh_token.payload.get('user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                new_access_token['user_id'] = user.id
                new_access_token['email'] = user.email
                new_access_token['role'] = user.role
                new_access_token['name'] = user.name
                new_access_token['is_superuser'] = user.is_superuser
            
            return {
                'access': str(new_access_token),
                'refresh': str(refresh_token) if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS') else None
            }
        except (TokenError, User.DoesNotExist):
            return None
    
    @staticmethod
    def blacklist_token(refresh_token_string):
        """Blacklist a refresh token"""
        try:
            token = RefreshToken(refresh_token_string)
            token.blacklist()
            return True
        except TokenError:
            return False
    
    @staticmethod
    def get_user_from_token(token_string):
        """Extract user information from a token"""
        try:
            payload = JWTManager.decode_token(token_string)
            if payload:
                return {
                    'user_id': payload.get('user_id'),
                    'email': payload.get('email'),
                    'role': payload.get('role'),
                    'name': payload.get('name'),
                    'is_superuser': payload.get('is_superuser', False)
                }
            return None
        except Exception:
            return None
