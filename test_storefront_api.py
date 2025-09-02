#!/usr/bin/env python
import os
import sys
import django

# Add the project root directory to the path
sys.path.append('d:/Codes/CampusLink')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.entrepreneurs_hub.views import StorefrontViewSet
from apps.entrepreneurs_hub.models import Owner, Storefront
import json

User = get_user_model()

def test_storefront_creation():
    """Test storefront creation to debug the 400 error"""
    
    # Check for entrepreneur users
    entrepreneur_users = User.objects.filter(role='entrepreneur')
    print(f"Found {entrepreneur_users.count()} entrepreneur users:")
    for user in entrepreneur_users:
        print(f"  - Username: {user.username}, Email: {user.email}, ID: {user.id}")
    
    if entrepreneur_users.exists():
        user = entrepreneur_users.first()
        print(f"\nTesting with user: {user.username or user.email}")
        
        # Create a request factory
        factory = RequestFactory()
        
        # Test data for creating a storefront
        test_data = {
            'name': 'Test Store',
            'description': 'A test storefront',
            'location': 'Test Location'
        }
        
        # Create a POST request without CSRF
        request = factory.post('/api/entrepreneurs_hub/storefronts/', 
                             data=json.dumps(test_data),
                             content_type='application/json')
        request.user = user
        request._dont_enforce_csrf_checks = True  # Disable CSRF for testing
        
        # Test the view
        view = StorefrontViewSet.as_view({'post': 'create'})
        
        try:
            response = view(request)
            print(f"Response status: {response.status_code}")
            print(f"Response data: {response.data}")
        except Exception as e:
            print(f"Error during storefront creation: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("No entrepreneur users found!")

    # Check Owner model
    print(f"\nOwner objects count: {Owner.objects.count()}")
    for owner in Owner.objects.all():
        print(f"  - {owner.name} (user: {owner.user})")
        
    # Check existing storefronts
    print(f"\nStorefront objects count: {Storefront.objects.count()}")
    for storefront in Storefront.objects.all():
        print(f"  - {storefront.name} (owner: {storefront.owner})")

if __name__ == '__main__':
    test_storefront_creation()
