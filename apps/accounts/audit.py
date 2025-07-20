"""
Audit logging and security monitoring for CampusLink
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()

class AuditAction(models.TextChoices):
    """Define audit action types"""
    LOGIN = 'LOGIN', 'User Login'
    LOGOUT = 'LOGOUT', 'User Logout'
    REGISTER = 'REGISTER', 'User Registration'
    PROFILE_UPDATE = 'PROFILE_UPDATE', 'Profile Update'
    PASSWORD_CHANGE = 'PASSWORD_CHANGE', 'Password Change'
    ROLE_CHANGE = 'ROLE_CHANGE', 'Role Change'
    PERMISSION_GRANT = 'PERMISSION_GRANT', 'Permission Granted'
    PERMISSION_REVOKE = 'PERMISSION_REVOKE', 'Permission Revoked'
    DATA_ACCESS = 'DATA_ACCESS', 'Data Access'
    DATA_MODIFY = 'DATA_MODIFY', 'Data Modification'
    UNAUTHORIZED_ACCESS = 'UNAUTHORIZED_ACCESS', 'Unauthorized Access Attempt'
    SUSPICIOUS_ACTIVITY = 'SUSPICIOUS_ACTIVITY', 'Suspicious Activity'

class AuditLog(models.Model):
    """Model for storing audit logs"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="User who performed the action"
    )
    
    action = models.CharField(
        max_length=50,
        choices=AuditAction.choices,
        help_text="Type of action performed"
    )
    
    resource = models.CharField(
        max_length=100,
        help_text="Resource that was accessed/modified"
    )
    
    resource_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="ID of the specific resource"
    )
    
    ip_address = models.GenericIPAddressField(
        help_text="IP address of the request"
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        help_text="User agent string"
    )
    
    details = models.JSONField(
        default=dict,
        help_text="Additional details about the action"
    )
    
    success = models.BooleanField(
        default=True,
        help_text="Whether the action was successful"
    )
    
    timestamp = models.DateTimeField(
        default=timezone.now,
        help_text="When the action occurred"
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"

class SecurityEvent(models.Model):
    """Model for storing security events and alerts"""
    
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    event_type = models.CharField(
        max_length=50,
        help_text="Type of security event"
    )
    
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='MEDIUM'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    ip_address = models.GenericIPAddressField()
    
    description = models.TextField(
        help_text="Description of the security event"
    )
    
    details = models.JSONField(
        default=dict,
        help_text="Additional event details"
    )
    
    resolved = models.BooleanField(
        default=False,
        help_text="Whether the event has been resolved"
    )
    
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.event_type} - {self.severity} at {self.timestamp}"

class AuditLogger:
    """Utility class for logging audit events"""
    
    @staticmethod
    def log_action(user, action, resource, request=None, **kwargs):
        """Log an audit action"""
        
        # Get IP address
        ip_address = '127.0.0.1'  # default
        user_agent = ''
        
        if request:
            ip_address = AuditLogger.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create audit log entry
        audit_log = AuditLog.objects.create(
            user=user,
            action=action,
            resource=resource,
            resource_id=kwargs.get('resource_id'),
            ip_address=ip_address,
            user_agent=user_agent,
            details=kwargs.get('details', {}),
            success=kwargs.get('success', True)
        )
        
        return audit_log
    
    @staticmethod
    def log_security_event(event_type, severity, description, request=None, user=None, **kwargs):
        """Log a security event"""
        
        ip_address = '127.0.0.1'  # default
        if request:
            ip_address = AuditLogger.get_client_ip(request)
        
        security_event = SecurityEvent.objects.create(
            event_type=event_type,
            severity=severity,
            user=user,
            ip_address=ip_address,
            description=description,
            details=kwargs.get('details', {})
        )
        
        return security_event
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def log_login(user, request, success=True):
        """Log user login attempt"""
        AuditLogger.log_action(
            user=user if success else None,
            action=AuditAction.LOGIN,
            resource='authentication',
            request=request,
            success=success,
            details={
                'email': getattr(user, 'email', 'unknown') if user else 'unknown'
            }
        )
        
        if not success:
            AuditLogger.log_security_event(
                event_type='FAILED_LOGIN',
                severity='MEDIUM',
                description='Failed login attempt',
                request=request,
                user=user
            )
    
    @staticmethod
    def log_unauthorized_access(user, resource, request):
        """Log unauthorized access attempt"""
        AuditLogger.log_action(
            user=user,
            action=AuditAction.UNAUTHORIZED_ACCESS,
            resource=resource,
            request=request,
            success=False
        )
        
        AuditLogger.log_security_event(
            event_type='UNAUTHORIZED_ACCESS',
            severity='HIGH',
            description=f'User {user} attempted unauthorized access to {resource}',
            request=request,
            user=user
        )
    
    @staticmethod
    def log_role_change(admin_user, target_user, old_role, new_role, request):
        """Log user role change"""
        AuditLogger.log_action(
            user=admin_user,
            action=AuditAction.ROLE_CHANGE,
            resource='user_management',
            resource_id=str(target_user.id),
            request=request,
            details={
                'target_user': target_user.email,
                'old_role': old_role,
                'new_role': new_role
            }
        )
    
    @staticmethod
    def log_data_access(user, resource, resource_id, request):
        """Log data access"""
        AuditLogger.log_action(
            user=user,
            action=AuditAction.DATA_ACCESS,
            resource=resource,
            resource_id=resource_id,
            request=request
        )
    
    @staticmethod
    def log_data_modification(user, resource, resource_id, request, changes=None):
        """Log data modification"""
        AuditLogger.log_action(
            user=user,
            action=AuditAction.DATA_MODIFY,
            resource=resource,
            resource_id=resource_id,
            request=request,
            details={
                'changes': changes or {}
            }
        )
