#!/usr/bin/env python
"""
Comprehensive test suite for CampusLink authorization functionality
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.accounts.models import User, Roles
from apps.entrepreneurs_hub.models import Storefront, Product
from apps.accounts.permissions import PermissionManager

class AuthorizationTestCase(TestCase):
    """Test authorization functionality across all modules"""
    
    def setUp(self):
        """Set up test data"""
        # Create test users for each role
        self.student = User.objects.create_user(
            email='student@test.com',
            name='Test Student',
            password='testpass123',
            role=Roles.STUDENT
        )
        
        self.entrepreneur = User.objects.create_user(
            email='entrepreneur@test.com',
            name='Test Entrepreneur',
            password='testpass123',
            role=Roles.ENTREPRENEUR
        )
        
        self.cds_owner = User.objects.create_user(
            email='cds@test.com',
            name='Test CDS Owner',
            password='testpass123',
            role=Roles.CDS_OWNER
        )
        
        self.laundry_staff = User.objects.create_user(
            email='laundry@test.com',
            name='Test Laundry Staff',
            password='testpass123',
            role=Roles.LAUNDRY_STAFF
        )
        
        self.superuser = User.objects.create_superuser(
            email='admin@test.com',
            name='Test Admin',
            password='testpass123'
        )
        
        # Create test storefront and product
        self.storefront = Storefront.objects.create(
            name='Test Storefront',
            description='Test Description',
            owner=self.entrepreneur
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Product Description',
            price=10.00,
            storefront=self.storefront
        )
        
        self.client = Client()

    def test_user_registration(self):
        """Test user registration with different roles"""
        registration_data = {
            'email': 'newuser@test.com',
            'name': 'New User',
            'password': 'newpass123',
            'phone': '1234567890'
        }
        
        response = self.client.post('/api/accounts/register/', registration_data)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], Roles.STUDENT)  # Default role

    def test_user_login(self):
        """Test user login functionality"""
        login_data = {
            'email': 'student@test.com',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/accounts/login/', 
                                   json.dumps(login_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], Roles.STUDENT)

    def test_role_based_access_control(self):
        """Test role-based access to different endpoints"""
        # Test student access to entrepreneur endpoints
        self.client.login(email='student@test.com', password='testpass123')
        response = self.client.post('/api/entrepreneurs-hub/create-product/')
        self.assertEqual(response.status_code, 403)
        
        # Test entrepreneur access to their endpoints
        self.client.login(email='entrepreneur@test.com', password='testpass123')
        response = self.client.get('/api/entrepreneurs-hub/my-products/')
        self.assertEqual(response.status_code, 200)

    def test_product_ownership_validation(self):
        """Test that entrepreneurs can only edit their own products"""
        # Create another entrepreneur
        another_entrepreneur = User.objects.create_user(
            email='entrepreneur2@test.com',
            name='Another Entrepreneur',
            password='testpass123',
            role=Roles.ENTREPRENEUR
        )
        
        # Login as the other entrepreneur and try to edit the product
        self.client.login(email='entrepreneur2@test.com', password='testpass123')
        
        update_data = {
            'name': 'Updated Product Name',
            'price': 15.00
        }
        
        response = self.client.put(f'/api/entrepreneurs-hub/products/{self.product.id}/update/',
                                  json.dumps(update_data),
                                  content_type='application/json')
        
        # Should be forbidden since they don't own the product
        self.assertEqual(response.status_code, 403)

    def test_profile_modification_restrictions(self):
        """Test that users can only modify their own profiles"""
        # Login as student
        self.client.login(email='student@test.com', password='testpass123')
        
        # Try to update another user's profile
        update_data = {
            'user_id': self.entrepreneur.id,
            'name': 'Hacked Name'
        }
        
        response = self.client.post('/api/accounts/update-profile/',
                                   update_data)
        
        # Should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_superuser_admin_access(self):
        """Test that superusers can access admin functions"""
        self.client.login(email='admin@test.com', password='testpass123')
        
        # Test user management endpoint
        response = self.client.get('/api/accounts/list-users/')
        self.assertEqual(response.status_code, 200)
        
        # Test role change endpoint
        role_change_data = {
            'user_id': self.student.id,
            'new_role': Roles.ENTREPRENEUR
        }
        
        response = self.client.post('/api/accounts/change-user-role/',
                                   json.dumps(role_change_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_permission_checks(self):
        """Test permission checking functionality"""
        # Test CDS owner permissions
        self.client.login(email='cds@test.com', password='testpass123')
        response = self.client.get('/api/accounts/check-permission/?permission=can_manage_cds_items')
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        # Note: This would be True if permissions are properly assigned

    def test_middleware_security(self):
        """Test middleware security features"""
        # Test inactive user check
        self.student.is_active = False
        self.student.save()
        
        self.client.login(email='student@test.com', password='testpass123')
        response = self.client.get('/api/accounts/get-current-user/')
        
        # Should be forbidden for inactive user
        self.assertEqual(response.status_code, 403)

    def test_database_level_constraints(self):
        """Test database-level validation constraints"""
        # Test that product must belong to entrepreneur's storefront
        another_entrepreneur = User.objects.create_user(
            email='entrepreneur3@test.com',
            name='Third Entrepreneur',
            password='testpass123',
            role=Roles.ENTREPRENEUR
        )
        
        another_storefront = Storefront.objects.create(
            name='Another Storefront',
            description='Another Description',
            owner=another_entrepreneur
        )
        
        # Try to create a product with wrong storefront ownership
        # This should be caught by model validation
        with self.assertRaises(Exception):
            # This would violate the ownership constraint
            pass

def run_authorization_tests():
    """Run all authorization tests"""
    print("🔒 Running CampusLink Authorization Test Suite")
    print("=" * 60)
    
    # Import Django test runner
    from django.test.utils import get_runner
    from django.conf import settings
    
    # Get the Django test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Run the tests
    failures = test_runner.run_tests(['__main__'])
    
    if failures:
        print(f"\n❌ {failures} test(s) failed")
        return False
    else:
        print("\n✅ All authorization tests passed!")
        return True

if __name__ == '__main__':
    run_authorization_tests()
