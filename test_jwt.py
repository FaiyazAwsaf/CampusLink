#!/usr/bin/env python3
"""
Simple test script to verify JWT authentication endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/accounts"

def test_jwt_endpoints():
    """Test JWT authentication endpoints"""
    
    print("🧪 Testing JWT Authentication Endpoints")
    print("=" * 50)
    
    # Test 1: JWT Registration
    print("\n1. Testing JWT Registration...")
    register_data = {
        "email": "testjwt@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "name": "JWT Test User",
        "phone": "01700000000"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/jwt/register/", json=register_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful")
            print(f"Access Token: {data['tokens']['access'][:50]}...")
            print(f"User: {data['user']['email']}")
            
            # Store tokens for further tests
            access_token = data['tokens']['access']
            refresh_token = data['tokens']['refresh']
            
        else:
            print(f"❌ Registration failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 2: JWT Current User
    print("\n2. Testing JWT Current User...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/jwt/current-user/", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Current user retrieval successful")
            print(f"User: {data['user']['email']}")
            print(f"Role: {data['user']['role']}")
        else:
            print(f"❌ Current user failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Current user error: {e}")
    
    # Test 3: JWT Token Refresh
    print("\n3. Testing JWT Token Refresh...")
    
    try:
        response = requests.post(f"{BASE_URL}/jwt/refresh/", json={"refresh": refresh_token})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Token refresh successful")
            print(f"New Access Token: {data['tokens']['access'][:50]}...")
            new_access_token = data['tokens']['access']
        else:
            print(f"❌ Token refresh failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Token refresh error: {e}")
        return
    
    # Test 4: JWT Login
    print("\n4. Testing JWT Login...")
    login_data = {
        "email": "testjwt@example.com",
        "password": "TestPass123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/jwt/login/", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful")
            print(f"Access Token: {data['tokens']['access'][:50]}...")
            print(f"User: {data['user']['email']}")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Test 5: JWT Logout (Token Blacklisting)
    print("\n5. Testing JWT Logout...")
    headers = {"Authorization": f"Bearer {new_access_token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/jwt/logout/", 
                               json={"refresh": refresh_token}, 
                               headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Logout successful")
        else:
            print(f"❌ Logout failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Logout error: {e}")
    
    # Test 6: Verify token is blacklisted
    print("\n6. Testing blacklisted token...")
    
    try:
        response = requests.post(f"{BASE_URL}/jwt/refresh/", json={"refresh": refresh_token})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Token successfully blacklisted")
        else:
            print(f"⚠️  Token should be blacklisted: {response.text}")
            
    except Exception as e:
        print(f"❌ Blacklist test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 JWT Authentication Test Complete!")

def test_permissions():
    """Test JWT permission endpoints"""
    
    print("\n🔐 Testing JWT Permission Endpoints")
    print("=" * 50)
    
    # First login as CDS Owner or create CDS Owner user
    print("\n1. Testing with regular user permissions...")
    
    # Register a regular user
    register_data = {
        "email": "regular@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "name": "Regular User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/jwt/register/", json=register_data)
        if response.status_code == 201:
            data = response.json()
            access_token = data['tokens']['access']
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test permission check
            response = requests.get(f"{BASE_URL}/jwt/check-permission/?permission=can_manage_users", 
                                  headers=headers)
            if response.status_code == 200:
                perm_data = response.json()
                print(f"✅ Permission check: {perm_data['has_permission']}")
            
            # Test get permissions
            response = requests.get(f"{BASE_URL}/jwt/get-permissions/", headers=headers)
            if response.status_code == 200:
                perm_data = response.json()
                print(f"✅ User permissions: {len(perm_data['permissions'])} permissions")
            
        else:
            print(f"❌ Regular user registration failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Permission test error: {e}")

if __name__ == "__main__":
    test_jwt_endpoints()
    test_permissions()
