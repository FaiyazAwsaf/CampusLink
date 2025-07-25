from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from .models import User


class UserRoles:
    """Constants for user roles"""
    ADMIN = 'admin'
    STAFF = 'staff'
    STUDENT = 'student'
    ENTREPRENEUR = 'entrepreneur'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (STUDENT, 'Student'),
        (ENTREPRENEUR, 'Entrepreneur'),
    ]


class PermissionManager:
    """Utility class for managing user permissions"""
    
    @staticmethod
    def create_custom_permissions():
        """Create custom permissions for the application"""
        try:
            content_type = ContentType.objects.get_for_model(User)
            
            # Define custom permissions
            permissions = [
                ('can_manage_users', 'Can manage users'),
                ('can_view_all_orders', 'Can view all orders'),
                ('can_manage_inventory', 'Can manage inventory'),
                ('can_process_orders', 'Can process orders'),
                ('can_view_analytics', 'Can view analytics'),
                ('can_manage_entrepreneurs', 'Can manage entrepreneurs'),
                ('can_create_products', 'Can create products'),
                ('can_manage_laundry', 'Can manage laundry services'),
            ]
            
            for codename, name in permissions:
                Permission.objects.get_or_create(
                    codename=codename,
                    name=name,
                    content_type=content_type,
                )
            
            return True
        except Exception as e:
            print(f"Error creating permissions: {e}")
            return False
    
    @staticmethod
    def create_user_groups():
        """Create user groups with appropriate permissions"""
        try:
            # Create groups
            admin_group, _ = Group.objects.get_or_create(name='Administrators')
            staff_group, _ = Group.objects.get_or_create(name='Staff')
            student_group, _ = Group.objects.get_or_create(name='Students')
            entrepreneur_group, _ = Group.objects.get_or_create(name='Entrepreneurs')
            
            # Get permissions
            content_type = ContentType.objects.get_for_model(User)
            
            # Admin permissions (all)
            admin_permissions = Permission.objects.filter(content_type=content_type)
            admin_group.permissions.set(admin_permissions)
            
            # Staff permissions
            staff_permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=[
                    'can_view_all_orders',
                    'can_process_orders',
                    'can_manage_inventory',
                    'can_manage_laundry'
                ]
            )
            staff_group.permissions.set(staff_permissions)
            
            # Entrepreneur permissions
            entrepreneur_permissions = Permission.objects.filter(
                content_type=content_type,
                codename__in=['can_create_products']
            )
            entrepreneur_group.permissions.set(entrepreneur_permissions)
            
            # Student group (basic permissions only)
            # Students don't get additional permissions beyond basic user rights
            
            return True
        except Exception as e:
            print(f"Error creating groups: {e}")
            return False
    
    @staticmethod
    def assign_user_to_group(user, group_name):
        """Assign user to a specific group"""
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            return True
        except Group.DoesNotExist:
            return False
    
    @staticmethod
    def remove_user_from_group(user, group_name):
        """Remove user from a specific group"""
        try:
            group = Group.objects.get(name=group_name)
            user.groups.remove(group)
            return True
        except Group.DoesNotExist:
            return False


class AuthorizationChecker:
    """Utility class for checking user authorization"""
    
    @staticmethod
    def can_access_user_data(requesting_user, target_user):
        """Check if requesting user can access target user's data"""
        if requesting_user == target_user:
            return True
        if requesting_user.is_admin or requesting_user.is_staff:
            return True
        return False
    
    @staticmethod
    def can_modify_user_data(requesting_user, target_user):
        """Check if requesting user can modify target user's data"""
        if requesting_user == target_user:
            return True
        if requesting_user.is_admin:
            return True
        return False
    
    @staticmethod
    def can_delete_user(requesting_user, target_user):
        """Check if requesting user can delete target user"""
        if requesting_user.is_admin and requesting_user != target_user:
            return True
        return False
    
    @staticmethod
    def can_manage_orders(user):
        """Check if user can manage orders"""
        return user.is_staff or user.is_admin or user.has_perm('accounts.can_process_orders')
    
    @staticmethod
    def can_view_all_orders(user):
        """Check if user can view all orders"""
        return user.is_admin or user.has_perm('accounts.can_view_all_orders')
    
    @staticmethod
    def can_manage_inventory(user):
        """Check if user can manage inventory"""
        return user.is_staff or user.is_admin or user.has_perm('accounts.can_manage_inventory')
    
    @staticmethod
    def can_create_products(user):
        """Check if user can create products"""
        return user.is_admin or user.has_perm('accounts.can_create_products')
    
    @staticmethod
    def get_user_permissions(user):
        """Get all permissions for a user"""
        if not user.is_authenticated:
            return []
        
        permissions = set()
        
        # Add user permissions
        for perm in user.user_permissions.all():
            permissions.add(perm.codename)
        
        # Add group permissions
        for group in user.groups.all():
            for perm in group.permissions.all():
                permissions.add(perm.codename)
        
        return list(permissions)
