#!/usr/bin/env python
"""
Test script to verify profile modification restrictions
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from apps.accounts.models import User, Roles

def test_profile_modification_restrictions():
    print("Testing profile modification restrictions...")
    
    # Create test users
    try:
        user1 = User.objects.get(email='user1@test.com')
    except User.DoesNotExist:
        user1 = User.objects.create_user(
            email='user1@test.com',
            name='User One',
            password='testpass123',
            role=Roles.STUDENT
        )
    
    try:
        user2 = User.objects.get(email='user2@test.com')
    except User.DoesNotExist:
        user2 = User.objects.create_user(
            email='user2@test.com',
            name='User Two',
            password='testpass123',
            role=Roles.ENTREPRENEUR
        )
    
    try:
        superuser = User.objects.get(email='superuser@test.com')
    except User.DoesNotExist:
        superuser = User.objects.create_superuser(
            email='superuser@test.com',
            name='Super User',
            password='testpass123'
        )
    
    print(f"Created test users:")
    print(f"  - User1: {user1.name} (role: {user1.role})")
    print(f"  - User2: {user2.name} (role: {user2.role})")
    print(f"  - Superuser: {superuser.name} (is_superuser: {superuser.is_superuser})")
    
    # Test profile modification permissions
    print("\n--- Testing profile modification permissions ---")
    
    # Test 1: User can modify their own profile
    print(f"User1 can modify own profile: {user1.can_modify_user_data(user1)}")  # Should be True
    
    # Test 2: User cannot modify another user's profile
    print(f"User1 can modify User2's profile: {user1.can_modify_user_data(user2)}")  # Should be False
    print(f"User2 can modify User1's profile: {user2.can_modify_user_data(user1)}")  # Should be False
    
    # Test 3: Superuser can modify any profile
    print(f"Superuser can modify User1's profile: {superuser.can_modify_user_data(user1)}")  # Should be True
    print(f"Superuser can modify User2's profile: {superuser.can_modify_user_data(user2)}")  # Should be True
    print(f"Superuser can modify own profile: {superuser.can_modify_user_data(superuser)}")  # Should be True
    
    # Test data access permissions (should be slightly different)
    print("\n--- Testing data access permissions ---")
    print(f"User1 can access own data: {user1.can_access_user_data(user1)}")  # Should be True
    print(f"User1 can access User2's data: {user1.can_access_user_data(user2)}")  # Should be False
    print(f"Superuser can access User1's data: {superuser.can_access_user_data(user1)}")  # Should be True
    
    # Test role-based access
    print("\n--- Testing role isolation ---")
    entrepreneur_users = User.objects.filter(role=Roles.ENTREPRENEUR)
    student_users = User.objects.filter(role=Roles.STUDENT)
    
    print(f"Total entrepreneurs: {entrepreneur_users.count()}")
    print(f"Total students: {student_users.count()}")
    
    print("\n✅ Profile modification restriction tests completed!")

if __name__ == '__main__':
    test_profile_modification_restrictions()
