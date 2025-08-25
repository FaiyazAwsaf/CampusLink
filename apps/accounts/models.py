from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with email as the unique identifier"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()  # This will run model validation
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
    def _validate_email(self, email):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None


class User(AbstractUser):
    """Custom User model with email as the unique identifier"""
    
    ROLE_CHOICES = [
        ('cds_owner', 'CDS Owner'),
        ('laundry_staff', 'Laundry Staff'),
        ('student', 'Student'),
        ('entrepreneur', 'Entrepreneur'),
    ]
    
    # Phone number validator
    phone_validator = RegexValidator(
        regex=r'^(\+88)?01[0-9]{9}$',
        message='Phone number must be in the format: +8801XXXXXXXXX or 01XXXXXXXXX'
    )
    
    # Name validator
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z\s.]+$',
        message='Name can only contain letters, spaces, and dots'
    )
    
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True, max_length=254)
    name = models.CharField(
        _('full name'), 
        max_length=255, 
        validators=[name_validator],
        help_text='Enter your full name (letters, spaces, and dots only)'
    )
    phone = models.CharField(
        _('phone number'), 
        max_length=15, 
        blank=True, 
        null=True,
        validators=[phone_validator],
        help_text='Enter phone number in format: +8801XXXXXXXXX or 01XXXXXXXXX'
    )
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'  # Make email the username field
    REQUIRED_FIELDS = ['name']  # Required fields for createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def clean(self):
        """Custom validation for the User model"""
        super().clean()
        
        # Validate name length
        if self.name and len(self.name.strip()) < 2:
            raise ValidationError({'name': 'Name must be at least 2 characters long'})
        
        # Validate name doesn't contain only spaces
        if self.name and not self.name.strip():
            raise ValidationError({'name': 'Name cannot be empty or contain only spaces'})
        
        # Validate phone number if provided
        if self.phone:
            # Remove spaces and dashes
            phone_clean = re.sub(r'[\s-]', '', self.phone)
            if not re.match(r'^(\+88)?01[0-9]{9}$', phone_clean):
                raise ValidationError({
                    'phone': 'Phone number must be in the format: +8801XXXXXXXXX or 01XXXXXXXXX'
                })
        
        # Validate email domain (basic check for common domains)
        if self.email:
            domain = self.email.split('@')[1].lower()
            # You can add more domain restrictions here if needed
            if len(domain) < 4:
                raise ValidationError({'email': 'Please enter a valid email address'})
    
    def save(self, *args, **kwargs):
        """Override save method to run validation"""
        # Clean the name field
        if self.name:
            self.name = self.name.strip()
        
        # Clean the phone field
        if self.phone:
            self.phone = re.sub(r'[\s-]', '', self.phone)
        
        # Run validation
        self.full_clean()
        super().save(*args, **kwargs)
    
    def has_role(self, role):
        """Check if user has a specific role"""
        return self.role == role
    
    def can_access_user_data(self, target_user):
        """Check if this user can access target user's data"""
        return self == target_user or self.is_admin or self.is_staff
    
    def can_modify_user_data(self, target_user):
        """Check if this user can modify target user's data"""
        return self == target_user or self.is_admin
    
    def get_permissions_list(self):
        """Get list of permissions for this user"""
        permissions = set()
        
        # Add user permissions
        for perm in self.user_permissions.all():
            permissions.add(perm.codename)
        
        # Add group permissions
        for group in self.groups.all():
            for perm in group.permissions.all():
                permissions.add(perm.codename)
        
        return list(permissions)
