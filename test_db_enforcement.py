#!/usr/bin/env python
"""
Test script to verify database-level enforcement of entrepreneur storefront ownership
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.exceptions import ValidationError
from apps.accounts.models import User, Roles
from apps.entrepreneurs_hub.models import Storefront, Product

def test_database_level_enforcement():
    print("Testing database-level enforcement...")
    
    # Create test users
    try:
        entrepreneur = User.objects.get(email='test_entrepreneur@example.com')
    except User.DoesNotExist:
        entrepreneur = User.objects.create_user(
            email='test_entrepreneur@example.com',
            name='Test Entrepreneur',
            password='testpass123',
            role=Roles.ENTREPRENEUR
        )
    
    try:
        student = User.objects.get(email='test_student@example.com')
    except User.DoesNotExist:
        student = User.objects.create_user(
            email='test_student@example.com',
            name='Test Student',
            password='testpass123',
            role=Roles.STUDENT
        )
    
    print(f"Created entrepreneur: {entrepreneur.name} (role: {entrepreneur.role})")
    print(f"Created student: {student.name} (role: {student.role})")
    
    # Test 1: Valid storefront creation (entrepreneur)
    print("\n--- Test 1: Valid storefront creation ---")
    try:
        valid_storefront = Storefront(name='Valid Store', owner=entrepreneur)
        valid_storefront.save()
        print("✅ Valid storefront created successfully")
    except ValidationError as e:
        print(f"❌ Unexpected validation error: {e}")
    
    # Test 2: Invalid storefront creation (non-entrepreneur)
    print("\n--- Test 2: Invalid storefront creation (student owner) ---")
    try:
        invalid_storefront = Storefront(name='Invalid Store', owner=student)
        invalid_storefront.save()
        print("❌ Invalid storefront was created (this should not happen!)")
    except ValidationError as e:
        print(f"✅ Validation correctly prevented invalid storefront: {e}")
    
    # Test 3: Valid product creation
    print("\n--- Test 3: Valid product creation ---")
    try:
        valid_product = Product(
            store_id=valid_storefront,
            name='Valid Product',
            category='Electronics',
            description='Test product',
            price=100.00
        )
        valid_product.save()
        print("✅ Valid product created successfully")
    except ValidationError as e:
        print(f"❌ Unexpected validation error: {e}")
    
    # Test 4: Test the is_owned_by method
    print("\n--- Test 4: Ownership validation ---")
    print(f"Product owned by entrepreneur: {valid_product.is_owned_by(entrepreneur)}")  # Should be True
    print(f"Product owned by student: {valid_product.is_owned_by(student)}")  # Should be False
    
    # Cleanup
    try:
        valid_product.delete()
        valid_storefront.delete()
        print("\n🧹 Cleanup completed")
    except:
        pass
    
    print("\n✅ Database-level enforcement test completed!")

if __name__ == '__main__':
    test_database_level_enforcement()
