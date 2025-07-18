from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import json


class AuthorizationMiddleware(MiddlewareMixin):
    """
    Middleware to handle authorization checks and security headers
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Process request before it reaches the view
        """
        # Add user IP to request for logging
        request.user_ip = self.get_client_ip(request)
        
        # Check for inactive users
        if request.user.is_authenticated and not request.user.is_active:
            return JsonResponse({
                'success': False,
                'error': 'Account is inactive'
            }, status=403)
        
        return None
    
    def process_response(self, request, response):
        """
        Process response before sending to client
        """
        # Add security headers
        if hasattr(settings, 'DEBUG') and not settings.DEBUG:
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
        
        return response
    
    def get_client_ip(self, request):
        """
        Get client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
