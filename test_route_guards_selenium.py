#!/usr/bin/env python
"""
Manual Route Guards Test Script
Tests authentication and authorization functionality via browser automation
"""
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RouteGuardsTest:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.base_url = "http://localhost:5173"
        self.wait = WebDriverWait(self.driver, 10)
        
        self.test_results = []

    def add_result(self, test_name, expected, actual, passed):
        self.test_results.append({
            'test': test_name,
            'expected': expected,
            'actual': actual,
            'passed': passed,
            'timestamp': time.strftime('%H:%M:%S')
        })
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}: Expected {expected}, Got {actual}")

    def clear_local_storage(self):
        """Clear authentication from localStorage"""
        self.driver.execute_script("localStorage.clear();")

    def set_test_user(self, role):
        """Set a test user in localStorage"""
        test_users = {
            'STUDENT': {
                'id': 1,
                'email': 'student@test.com',
                'name': 'Test Student',
                'role': 'STUDENT',
                'is_superuser': False
            },
            'ENTREPRENEUR': {
                'id': 2,
                'email': 'entrepreneur@test.com',
                'name': 'Test Entrepreneur',
                'role': 'ENTREPRENEUR',
                'is_superuser': False
            },
            'CDS_OWNER': {
                'id': 3,
                'email': 'cds@test.com',
                'name': 'Test CDS Owner',
                'role': 'CDS_OWNER',
                'is_superuser': False
            },
            'LAUNDRY_STAFF': {
                'id': 4,
                'email': 'laundry@test.com',
                'name': 'Test Laundry Staff',
                'role': 'LAUNDRY_STAFF',
                'is_superuser': False
            }
        }
        
        user_data = json.dumps(test_users[role])
        self.driver.execute_script(f"localStorage.setItem('user', '{user_data}');")

    def test_route_access(self, route, expected_behavior, user_role=None):
        """Test access to a specific route"""
        try:
            if user_role:
                self.set_test_user(user_role)
            else:
                self.clear_local_storage()
            
            # Navigate to the route
            self.driver.get(f"{self.base_url}{route}")
            time.sleep(1)  # Wait for route resolution
            
            current_url = self.driver.current_url
            current_path = current_url.replace(self.base_url, '')
            
            # Check if we're at the expected location
            if expected_behavior == 'accessible':
                passed = current_path == route
                self.add_result(
                    f"Access {route} as {user_role or 'guest'}",
                    f"Stay at {route}",
                    f"At {current_path}",
                    passed
                )
            elif expected_behavior == 'redirect_login':
                passed = current_path == '/login'
                self.add_result(
                    f"Access {route} as {user_role or 'guest'}",
                    "Redirect to /login",
                    f"At {current_path}",
                    passed
                )
            elif expected_behavior == 'redirect_unauthorized':
                passed = current_path == '/unauthorized'
                self.add_result(
                    f"Access {route} as {user_role or 'guest'}",
                    "Redirect to /unauthorized",
                    f"At {current_path}",
                    passed
                )
            elif expected_behavior == 'redirect_home':
                passed = current_path == '/home'
                self.add_result(
                    f"Access {route} as {user_role or 'guest'}",
                    "Redirect to /home",
                    f"At {current_path}",
                    passed
                )
                
        except Exception as e:
            self.add_result(
                f"Access {route} as {user_role or 'guest'}",
                expected_behavior,
                f"Error: {str(e)}",
                False
            )

    def run_comprehensive_tests(self):
        """Run all route guard tests"""
        print("🔒 Starting Comprehensive Route Guards Testing")
        print("=" * 60)
        
        # Test cases: (route, expected_behavior_by_role)
        test_cases = [
            # Public routes
            ('/', {
                None: 'accessible',
                'STUDENT': 'accessible',
                'ENTREPRENEUR': 'accessible',
                'CDS_OWNER': 'accessible',
                'LAUNDRY_STAFF': 'accessible'
            }),
            
            # Guest-only routes
            ('/login', {
                None: 'accessible',
                'STUDENT': 'redirect_home',
                'ENTREPRENEUR': 'redirect_home',
                'CDS_OWNER': 'redirect_home',
                'LAUNDRY_STAFF': 'redirect_home'
            }),
            
            ('/register', {
                None: 'accessible',
                'STUDENT': 'redirect_home',
                'ENTREPRENEUR': 'redirect_home',
                'CDS_OWNER': 'redirect_home',
                'LAUNDRY_STAFF': 'redirect_home'
            }),
            
            # Authenticated routes
            ('/home', {
                None: 'redirect_login',
                'STUDENT': 'accessible',
                'ENTREPRENEUR': 'accessible',
                'CDS_OWNER': 'accessible',
                'LAUNDRY_STAFF': 'accessible'
            }),
            
            ('/profile', {
                None: 'redirect_login',
                'STUDENT': 'accessible',
                'ENTREPRENEUR': 'accessible',
                'CDS_OWNER': 'accessible',
                'LAUNDRY_STAFF': 'accessible'
            }),
            
            # Role-specific routes
            ('/cds/admin', {
                None: 'redirect_login',
                'STUDENT': 'redirect_unauthorized',
                'ENTREPRENEUR': 'redirect_unauthorized',
                'CDS_OWNER': 'accessible',
                'LAUNDRY_STAFF': 'redirect_unauthorized'
            }),
            
            ('/laundry/admin', {
                None: 'redirect_login',
                'STUDENT': 'redirect_unauthorized',
                'ENTREPRENEUR': 'redirect_unauthorized',
                'CDS_OWNER': 'redirect_unauthorized',
                'LAUNDRY_STAFF': 'accessible'
            }),
            
            ('/entrepreneur/dashboard', {
                None: 'redirect_login',
                'STUDENT': 'redirect_unauthorized',
                'ENTREPRENEUR': 'accessible',
                'CDS_OWNER': 'redirect_unauthorized',
                'LAUNDRY_STAFF': 'redirect_unauthorized'
            }),
        ]
        
        # Run tests
        for route, role_behaviors in test_cases:
            print(f"\n--- Testing route: {route} ---")
            for role, expected_behavior in role_behaviors.items():
                self.test_route_access(route, expected_behavior, role)
        
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = len([r for r in self.test_results if r['passed']])
        total = len(self.test_results)
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%" if total > 0 else "No tests run")
        
        if failed > 0:
            print(f"\n📋 FAILED TESTS:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"❌ {result['test']}: Expected {result['expected']}, Got {result['actual']}")
        
        print("\n🎯 ROUTE GUARDS TEST COMPLETED")

    def cleanup(self):
        """Clean up resources"""
        self.driver.quit()

def main():
    print("🚀 Initializing Route Guards Test Suite")
    print("Make sure both servers are running:")
    print("- Frontend: http://localhost:5173")
    print("- Backend: http://127.0.0.1:8000")
    print()
    
    input("Press Enter to start testing...")
    
    test_runner = RouteGuardsTest()
    
    try:
        test_runner.run_comprehensive_tests()
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n💥 Testing failed with error: {e}")
    finally:
        test_runner.cleanup()

if __name__ == "__main__":
    main()
