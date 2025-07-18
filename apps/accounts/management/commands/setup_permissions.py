from django.core.management.base import BaseCommand
from apps.accounts.permissions import PermissionManager


class Command(BaseCommand):
    help = 'Initialize permissions and user groups for the application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing permissions and groups...'))
        
        # Create custom permissions
        if PermissionManager.create_custom_permissions():
            self.stdout.write(self.style.SUCCESS('✓ Custom permissions created successfully'))
        else:
            self.stdout.write(self.style.ERROR('✗ Failed to create custom permissions'))
        
        # Create user groups
        if PermissionManager.create_user_groups():
            self.stdout.write(self.style.SUCCESS('✓ User groups created successfully'))
        else:
            self.stdout.write(self.style.ERROR('✗ Failed to create user groups'))
        
        self.stdout.write(self.style.SUCCESS('Authorization setup completed!'))
