from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with email as the unique identifier"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as the unique identifier"""
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=255)
    phone = models.CharField(_('phone number'), max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'  # Make email the username field
    REQUIRED_FIELDS = ['name']  # Required fields for createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email
