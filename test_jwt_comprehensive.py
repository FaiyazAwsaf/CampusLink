#!/usr/bin/env python3
"""
Comprehensive JWT Authentication Test Suite for CampusLink
Tests all JWT endpoints and authentication flows
"""

import requests
import json
import sys
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api/accounts"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestResults:
    """Track test results"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self, test_name):
        self.total += 1
        self.passed += 1
        print(f"{Colors.GREEN}✅ PASS{Colors.END}: {test_name}")

    def add_fail(self, test_name, error):
        self.total += 1
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"{Colors.RED}❌ FAIL{Colors.END}: {test_name}")
        print(f"   {Colors.RED}Error: {error}{Colors.END}")

    def print_summary(self):
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}TEST SUMMARY{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"Total Tests: {self.total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.END}")
        
        if self.failed > 0:
            print(f"\n{Colors.RED}FAILED TESTS:{Colors.END}")
            for error in self.errors:
                print(f"  - {error}")
        
        success_rate = (self.passed / self.total * 100) if self.total > 0 else 0
        print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.END}")

def test_server_health():
    """Test if backend server is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False

def cleanup_test_users():
    """Clean up test users (requires admin access)"""
    try:
        # This would require admin credentials, skip for now
        pass
    except:
        pass

def test_jwt_registration(results):
    """Test JWT user registration"""
    test_name = "JWT User Registration"
    
    # Generate unique email for testing
    timestamp = str(int(time.time()))
    test_email = f"testuser{timestamp}@example.com"
    
    registration_data = {
        "email": test_email,
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "name": "Test User",
        "phone": "01700000000"
    }
    
    try:
        response = requests.post(f"{API_BASE}/jwt/register/", json=registration_data)
        
        if response.status_code == 201:
            data = response.json()
            if data.get('success') and 'tokens' in data and 'user' in data:
                results.add_pass(test_name)
                return data['tokens'], data['user']
            else:
                results.add_fail(test_name, f"Invalid response structure: {data}")
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))
    
    return None, None

def test_jwt_login(results, user_email="testjwt@example.com", password="TestPass123!"):
    """Test JWT user login"""
    test_name = "JWT User Login"
    
    login_data = {
        "email": user_email,
        "password": password
    }
    
    try:
        response = requests.post(f"{API_BASE}/jwt/login/", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'tokens' in data and 'user' in data:
                results.add_pass(test_name)
                return data['tokens'], data['user']
            else:
                results.add_fail(test_name, f"Invalid response structure: {data}")
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))
    
    return None, None

def test_jwt_current_user(results, tokens):
    """Test JWT current user endpoint"""
    test_name = "JWT Current User"
    
    if not tokens:
        results.add_fail(test_name, "No tokens available")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access']}"}
    
    try:
        response = requests.get(f"{API_BASE}/jwt/current-user/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'user' in data:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Invalid response structure: {data}")
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))

def test_jwt_token_refresh(results, tokens):
    """Test JWT token refresh"""
    test_name = "JWT Token Refresh"
    
    if not tokens:
        results.add_fail(test_name, "No tokens available")
        return None
    
    refresh_data = {"refresh": tokens['refresh']}
    
    try:
        response = requests.post(f"{API_BASE}/jwt/refresh/", json=refresh_data)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'tokens' in data:
                results.add_pass(test_name)
                return data['tokens']
            else:
                results.add_fail(test_name, f"Invalid response structure: {data}")
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))
    
    return None

def test_jwt_permissions(results, tokens):
    """Test JWT permission endpoints"""
    test_name = "JWT Permission Check"
    
    if not tokens:
        results.add_fail(test_name, "No tokens available")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access']}"}
    
    try:
        # Test permission check
        response = requests.get(f"{API_BASE}/jwt/check-permission/?permission=can_manage_users", 
                              headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'has_permission' in data:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Invalid response structure: {data}")
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))

def test_jwt_get_permissions(results, tokens):
    """Test JWT get permissions endpoint"""
    test_name = "JWT Get Permissions"
    
    if not tokens:
        results.add_fail(test_name, "No tokens available")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access']}"}
    
    try:
        response = requests.get(f"{API_BASE}/jwt/get-permissions/", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'permissions' in data:
                results.add_pass(test_name)
            else:
                results.add_fail(test_name, f"Invalid response structure: {data}")
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))

def test_jwt_logout(results, tokens):
    """Test JWT logout (token blacklisting)"""
    test_name = "JWT Logout"
    
    if not tokens:
        results.add_fail(test_name, "No tokens available")
        return
    
    headers = {"Authorization": f"Bearer {tokens['access']}"}
    logout_data = {"refresh": tokens['refresh']}
    
    try:
        response = requests.post(f"{API_BASE}/jwt/logout/", 
                               json=logout_data, 
                               headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results.add_pass(test_name)
                return True
            else:
                results.add_fail(test_name, f"Invalid response structure: {data}")
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))
    
    return False

def test_blacklisted_token(results, tokens):
    """Test that blacklisted token cannot be used"""
    test_name = "Blacklisted Token Rejection"
    
    if not tokens:
        results.add_fail(test_name, "No tokens available")
        return
    
    refresh_data = {"refresh": tokens['refresh']}
    
    try:
        response = requests.post(f"{API_BASE}/jwt/refresh/", json=refresh_data)
        
        # Should fail with 401 or similar
        if response.status_code == 401:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 401, got {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))

def test_invalid_credentials(results):
    """Test login with invalid credentials"""
    test_name = "Invalid Credentials Rejection"
    
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{API_BASE}/jwt/login/", json=login_data)
        
        # Should fail with 400 or 401
        if response.status_code in [400, 401]:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 400/401, got {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))

def test_unauthorized_access(results):
    """Test accessing protected endpoint without token"""
    test_name = "Unauthorized Access Rejection"
    
    try:
        response = requests.get(f"{API_BASE}/jwt/current-user/")
        
        # Should fail with 401
        if response.status_code == 401:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Expected 401, got {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))

def test_token_verification(results, tokens):
    """Test JWT token verification"""
    test_name = "JWT Token Verification"
    
    if not tokens:
        results.add_fail(test_name, "No tokens available")
        return
    
    verify_data = {"token": tokens['access']}
    
    try:
        response = requests.post(f"{API_BASE}/jwt/verify/", json=verify_data)
        
        if response.status_code == 200:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        results.add_fail(test_name, str(e))

def main():
    """Run all tests"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("🧪 CampusLink JWT Authentication Test Suite")
    print(f"{'='*50}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}{Colors.END}")
    
    results = TestResults()
    
    # Check server health
    print(f"\n{Colors.YELLOW}🔍 Checking server health...{Colors.END}")
    if not test_server_health():
        print(f"{Colors.RED}❌ Backend server is not running at {BASE_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Please start the server with: python manage.py runserver 8000{Colors.END}")
        sys.exit(1)
    
    print(f"{Colors.GREEN}✅ Server is running{Colors.END}")
    
    # Run authentication flow tests
    print(f"\n{Colors.BLUE}{Colors.BOLD}🔐 Authentication Flow Tests{Colors.END}")
    
    # Test registration (creates new user each time)
    tokens, user = test_jwt_registration(results)
    
    # Test login with existing user (fallback)
    if not tokens:
        print(f"{Colors.YELLOW}Falling back to existing user login...{Colors.END}")
        tokens, user = test_jwt_login(results)
    
    # Test current user endpoint
    test_jwt_current_user(results, tokens)
    
    # Test token refresh
    new_tokens = test_jwt_token_refresh(results, tokens)
    if new_tokens:
        tokens = new_tokens
    
    # Test permission endpoints
    print(f"\n{Colors.BLUE}{Colors.BOLD}🔒 Permission Tests{Colors.END}")
    test_jwt_permissions(results, tokens)
    test_jwt_get_permissions(results, tokens)
    
    # Test token verification
    test_token_verification(results, tokens)
    
    # Test security features
    print(f"\n{Colors.BLUE}{Colors.BOLD}🛡️ Security Tests{Colors.END}")
    test_invalid_credentials(results)
    test_unauthorized_access(results)
    
    # Test logout and token blacklisting
    logout_success = test_jwt_logout(results, tokens)
    if logout_success:
        test_blacklisted_token(results, tokens)
    
    # Print final results
    results.print_summary()
    
    # Return exit code based on results
    if results.failed > 0:
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! JWT authentication is working correctly.{Colors.END}")
        sys.exit(0)

if __name__ == "__main__":
    main()
