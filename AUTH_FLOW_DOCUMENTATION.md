# CampusLink Authentication Flow Documentation

## Overview
CampusLink implements a comprehensive role-based authentication system using Django backend with **JWT (JSON Web Token) authentication** and Vue.js frontend. The system supports four user roles: Admin, Staff, Student, and Entrepreneur.

## 🔄 **Migration: Session to JWT Authentication**
As of August 2025, CampusLink has migrated from session-based authentication to JWT tokens for improved scalability, stateless authentication, and better support for mobile applications and API integrations.

## Architecture Components

### 1. Backend Authentication System (Django)

#### **Custom User Model (`apps/accounts/models.py`)**
- **Base**: Extends `AbstractUser` 
- **Username Field**: Email (username field removed)
- **Roles**: Admin, Staff, Student, Entrepreneur
- **Key Features**:
  - Email-based authentication
  - Phone number validation (Bangladesh format)
  - Profile image upload
  - Role-based permissions
  - Account verification status
- **Primary Fields**: Email (unique identifier), role, verification status, admin flag

#### **JWT Authentication Views (`apps/accounts/jwt_views.py`)**

**JWT Registration Flow:**
- Validate form data (email, password, name, phone, image)
- Create user with CustomUserManager
- Assign to default group (Students)
- Generate JWT access & refresh tokens
- Return user data + JWT tokens

**JWT Login Flow:**
- Validate credentials (email/password)
- Check account status (is_active)
- Authenticate using custom JWT serializer
- Generate JWT access & refresh tokens
- Return user data + JWT tokens

**JWT Token Management:**
- Refresh access token using refresh token
- Blacklist refresh token (secure logout)
- Verify token validity
- Get current user info (JWT protected)

#### **JWT Serializers (`apps/accounts/serializers.py`)**

**Custom JWT Login Serializer:**
- Uses email field instead of username for authentication
- Validates credentials against user database
- Generates access and refresh tokens upon successful authentication
- Returns user data along with JWT tokens
- Handles authentication errors gracefully

**JWT Registration Serializer:**
- Validates registration form data
- Creates new user account with provided information
- Automatically generates JWT tokens for immediate login
- Returns user data with tokens for seamless onboarding
- Integrates with user groups and permissions system

#### **Permission System (`apps/accounts/permissions.py`)**

**Custom Permissions:**
- `can_manage_users` - User management
- `can_view_all_orders` - View all orders
- `can_manage_inventory` - Inventory management
- `can_process_orders` - Order processing
- `can_view_analytics` - Analytics access
- `can_manage_entrepreneurs` - Entrepreneur management
- `can_create_products` - Product creation
- `can_manage_laundry` - Laundry service management

**User Groups & Permissions:**
- **Admin Group**: All permissions
- **Staff Group**: can_view_all_orders, can_process_orders, can_manage_inventory, can_manage_laundry
- **Entrepreneur Group**: can_create_products
- **Student Group**: Basic user permissions only

#### **JWT Authorization Decorators (`apps/accounts/decorators.py`)**
- `@jwt_login_required` - Requires valid JWT token
- `@admin_required` - Admin role required (JWT-based)
- `@staff_required` - Staff privileges required (JWT-based)
- `@permission_required(permission)` - Specific permission required (JWT-based)
- `@user_owns_resource(get_resource_user)` - Resource ownership check (JWT-based)

**JWT Token Validation:**
- Extracts Bearer token from Authorization header
- Validates token signature and expiration
- Returns appropriate error responses for invalid tokens
- Integrates with Django's user authentication system

#### **Validation System (`apps/accounts/validators.py`)**
Comprehensive validation for:
- **Email**: Format validation, uniqueness check
- **Password**: 8+ chars, uppercase, lowercase, number, special char
- **Phone**: Bangladesh format (+8801XXXXXXXXX or 01XXXXXXXXX)
- **Name**: Letters, spaces, dots only
- **Images**: Max 5MB, JPG/PNG/GIF only

### 2. Frontend JWT Authentication System (Vue.js)

#### **JWT Token Management (`frontend/src/utils/auth.js`)**
**TokenManager Class**: Centralized JWT token management
- Get and set access/refresh tokens from localStorage
- Clear tokens on logout
- Validate token expiration status
- Check if token will expire soon (for proactive refresh)
- Parse JWT payload for user information

**AuthService Class**: API authentication operations
- Login with email/password, store JWT tokens
- Register new users with automatic JWT token generation
- Logout with refresh token blacklisting
- Refresh access tokens using refresh tokens
- Handle authentication errors and token validation

#### **Pinia Authentication Store (`frontend/src/stores/auth.js`)**
**Reactive JWT State Management:**
- Initialize authentication state from localStorage and validate tokens
- Login action that handles credentials and stores JWT tokens
- Logout action that blacklists tokens and clears state
- Permission checking using user data from JWT
- Reactive user and authentication status tracking
- Automatic state persistence and recovery

#### **Axios JWT Configuration (`frontend/src/main.js`)**
**Request Interceptor**: Automatically adds JWT Bearer token to all API requests

**Response Interceptor**: Handles token refresh on 401 errors
- Queues failed requests during token refresh process
- Automatically retries failed requests with new tokens
- Logs out user if refresh token is invalid or expired
- Redirects to login page on authentication failure

**Automatic Token Refresh**: Background process that refreshes tokens every minute
- Checks token expiration status periodically
- Proactively refreshes tokens before they expire
- Handles refresh failures gracefully

#### **Vue Router Guards (`frontend/src/router/index.js`)**
**JWT-based route protection:**
- Initialize authentication state on route navigation
- Protect routes requiring authentication by checking JWT token validity
- Redirect unauthenticated users to login with return URL
- Prevent authenticated users from accessing guest-only pages
- Support for next parameter to redirect after successful login

#### **Authentication Components**

**Login Page (`frontend/src/views/LoginPage.vue`)**
- Uses Pinia auth store for JWT-based login
- Handles return URL from query parameters for seamless navigation
- Displays appropriate error messages for failed authentication
- Integrates with real-time form validation

**Register Page (`frontend/src/views/RegisterPage.vue`)**
- Real-time validation with backend synchronization
- File upload support for profile images  
- JWT token generation on successful registration
- Automatic login and redirect after registration
- Comprehensive error handling and user feedback

**Navigation Bar (`frontend/src/components/NavBar.vue`)**
- Reactive authentication state using Pinia store
- Dynamic UI elements based on JWT authentication status
- User profile display with data from JWT tokens
- Secure logout with token blacklisting

## 3. Authentication Flow Diagrams

### **JWT Registration Flow**
```
User (Frontend) → Validation → Backend API → Database → JWT Generation → Response
    ↓                ↓             ↓            ↓            ↓                ↓
1. Fill form    2. Client-side  3. Server    4. Create    5. Generate     6. Auto-login
   Submit          validation     validation    user         JWT tokens     + redirect
```

### **JWT Login Flow**
```
User → Frontend → Backend API → JWT Auth → Database → JWT Tokens → Frontend
  ↓       ↓           ↓            ↓          ↓           ↓            ↓
Enter → Validate → Authenticate → Verify   → Lookup → Generate    → Store tokens
creds   input      credentials    token      user     access/refresh  + user data
```

### **JWT Authorization Flow**
```
Request → JWT Token → Middleware → Decorator → Permission Check → View → Response
   ↓         ↓           ↓           ↓             ↓            ↓        ↓
API Call → Bearer     → Token      → Role/Perm → Database     → Execute → Success/
          Header      Validation   Validation   lookup        logic    Deny
```

### **JWT Token Refresh Flow**
```
Expired Token → Interceptor → Refresh API → New Access Token → Retry Request
      ↓             ↓             ↓              ↓                ↓
Auto-detected → Queue failed → Use refresh → Update storage → Continue operation
              requests       token                           seamlessly
```

## 4. Security Features

### **Backend JWT Security**
- **Token-Based Authentication**: Stateless JWT tokens (no server-side sessions)
- **Token Blacklisting**: Secure logout with refresh token blacklisting
- **Automatic Expiry**: Access tokens expire in 5 minutes, refresh tokens in 7 days
- **Token Rotation**: New access tokens generated automatically
- **Password Hashing**: Django's built-in PBKDF2
- **Input Validation**: Comprehensive validation system
- **Permission Checks**: Role-based access control
- **Account Security**: Active/inactive status checks

### **Frontend JWT Security**
- **Bearer Token Headers**: Automatic Authorization header injection
- **Secure Token Storage**: JWT tokens in localStorage (consider httpOnly cookies for production)
- **Automatic Refresh**: Transparent token refresh before expiry
- **Request Retry**: Failed requests retried with new tokens
- **Token Validation**: Client-side token expiry checking
- **Auto-logout**: Automatic logout on refresh token failure

## 5. Database Schema

### **User Model Fields**
- Email: Unique identifier, VARCHAR(254), required
- Password: Hashed password, VARCHAR(128), required
- Account Status: is_active (boolean), is_verified (boolean)
- Role Information: role (varchar), is_admin (boolean)
- Profile Data: name, phone, image
- Timestamps: created_at, updated_at

### **JWT Token Tables**
- Access tokens: Short-lived, not stored in database
- Refresh tokens: Stored in token_blacklist tables
- Blacklisted tokens: Managed by djangorestframework-simplejwt
- Token rotation: Automatic cleanup of expired blacklisted tokens

### **Permissions & Groups**
- Django's built-in auth tables: auth_permission, auth_group
- Group permissions: auth_group_permissions
- User groups: auth_user_groups
- User permissions: auth_user_user_permissions

## 6. API Endpoints

### **JWT Authentication Endpoints**
- POST /api/accounts/jwt/register/ - User registration with JWT tokens
- POST /api/accounts/jwt/login/ - User login with JWT tokens  
- POST /api/accounts/jwt/refresh/ - Refresh access token
- POST /api/accounts/jwt/logout/ - Blacklist refresh token (secure logout)
- POST /api/accounts/jwt/verify/ - Verify token validity
- GET /api/accounts/current-user/ - Get current user info (JWT protected)
- POST /api/accounts/update-profile/ - Update user profile (JWT protected)

### **Legacy Session Endpoints** (Deprecated)
- POST /api/accounts/register/ - [DEPRECATED] Session-based registration
- POST /api/accounts/login/ - [DEPRECATED] Session-based login  
- POST /api/accounts/logout/ - [DEPRECATED] Session-based logout
- GET /api/accounts/csrf/ - [DEPRECATED] Get CSRF token

### **Admin Endpoints** (Admin only)
- GET /api/accounts/list-users/ - List all users
- POST /api/accounts/change-role/ - Change user role
- POST /api/accounts/toggle-status/ - Toggle user active status

### **Permission Endpoints**
- GET /api/accounts/check-permission/ - Check specific permission
- GET /api/accounts/get-permissions/ - Get user permissions

## 7. Configuration Files

### **Django JWT Settings (`backend/settings.py`)**
**SIMPLE_JWT Configuration:**
- ACCESS_TOKEN_LIFETIME: 5 minutes for security
- REFRESH_TOKEN_LIFETIME: 7 days with rotation
- BLACKLIST_AFTER_ROTATION: True for secure logout
- ALGORITHM: HS256 with SECRET_KEY signing
- AUTH_HEADER_TYPES: Bearer token authentication

**REST Framework JWT Authentication:**
- DEFAULT_AUTHENTICATION_CLASSES: JWTAuthentication primary, SessionAuthentication fallback
- DEFAULT_PERMISSION_CLASSES: IsAuthenticated for protected endpoints

**CORS Settings for JWT:**
- CORS_ALLOW_CREDENTIALS: True for token transmission
- CORS_ALLOWED_ORIGINS: Frontend development and production URLs
- CORS_ALLOW_HEADERS: Authorization, Content-Type, and other required headers

**Required Apps for JWT:**
- rest_framework_simplejwt: Core JWT functionality
- rest_framework_simplejwt.token_blacklist: Token blacklisting support

### **URL Configuration (`backend/urls.py` & `apps/accounts/urls.py`)**
**Main URLs:**
- Main URL patterns include accounts API routes
- All authentication endpoints are namespaced under /api/accounts/

**JWT-specific URLs in accounts/urls.py:**
- JWT endpoints for login, refresh, verify, register, and logout
- Custom views extending djangorestframework-simplejwt functionality
- Integration with existing permission and user management systems

**URL Pattern Structure:**
- JWT endpoints: /api/accounts/jwt/* for new authentication
- Legacy endpoints: /api/accounts/* for backward compatibility (deprecated)
- Admin endpoints: /api/accounts/* for user management functions

## 8. Setup and Initialization

### **JWT Migration Command**
**Install JWT packages:**
- pip install djangorestframework-simplejwt

**Apply JWT-related migrations:**
- python manage.py migrate (applies JWT blacklist tables)

**Setup permissions (still required):**
- python manage.py setup_permissions (creates user groups and permissions)

### **Migration Files**
- 0001_initial.py - Initial user model
- 0002_user_created_at_user_is_verified_user_role_and_more.py - Additional fields
- JWT blacklist migrations are handled automatically by rest_framework_simplejwt.token_blacklist

## 9. Impact Analysis

### **Where JWT Authentication is Used**

1. **Navigation Bar**: JWT-based authentication state with reactive updates
2. **All Service Pages**: JWT token-based access control
3. **Profile Management**: JWT-protected user data management
4. **Order Systems**: JWT-authenticated user-specific data
5. **Admin Functions**: JWT-based role and permission checks
6. **API Security**: All endpoints protected with Bearer token authentication

### **Cross-App JWT Integration**
- **CDS App**: JWT-authenticated user orders and cart management
- **Laundry App**: JWT-protected user order management
- **Entrepreneur Hub**: JWT-based role verification for product creation
- **All Apps**: JWT token validation for user identification and permissions

## 10. Error Handling

### **Backend JWT Error Responses**
- JWT Authentication errors: Token validation failures, missing credentials
- JWT Token errors: Blacklisted tokens, expired tokens
- Validation errors: Email uniqueness, password requirements (unchanged from session auth)

### **Frontend JWT Error Handling**
- **Token Expiry**: Automatic refresh with retry logic
- **Network Errors**: Graceful degradation with user feedback  
- **Invalid Tokens**: Automatic logout and redirect to login
- **Refresh Failure**: Secure logout with token cleanup
- **Form Validation**: Real-time validation with backend sync
- **API Errors**: User-friendly error messages with proper formatting

## 11. Implementation Details

### **Custom User Manager (`apps/accounts/models.py`)**
```python
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()  # Run model validation
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(email, password, **extra_fields)
```

### **User Model Validation**
```python
def clean(self):
    """Custom validation for the User model"""
    super().clean()
    
    # Validate name length
    if self.name and len(self.name.strip()) < 2:
        raise ValidationError({'name': 'Name must be at least 2 characters long'})
    
    # Validate phone number if provided
    if self.phone:
        phone_clean = re.sub(r'[\s-]', '', self.phone)
        if not re.match(r'^(\+88)?01[0-9]{9}$', phone_clean):
            raise ValidationError({
                'phone': 'Phone number must be in the format: +8801XXXXXXXXX or 01XXXXXXXXX'
            })
```

### **JWT Token Lifecycle**
**JWT Token Structure:**
- Header: Token type and algorithm information
- Payload: User ID, expiration timestamp, issued timestamp, JWT ID for blacklisting
- Signature: Cryptographic signature for validation
- Access Token: 5 minutes lifetime for security
- Refresh Token: 7 days lifetime with automatic rotation
- Blacklisting: Secure logout prevents token reuse

**JWT Authentication Flow:**
- Token extraction from Authorization Bearer header
- Signature and expiration validation
- User identification from token payload
- Permission and role verification
- Automatic token refresh when nearing expiration

### **JWT Route Protection**
**Router Configuration with JWT Guards:**
- Routes marked with `requiresAuth` meta property require valid JWT tokens
- Routes marked with `guestOnly` meta property redirect authenticated users
- Service routes (CDS, Laundry, Entrepreneur Hub) require authentication
- Profile and admin routes have role-based access requirements

**JWT Navigation Guards:**
- Initialize authentication state from JWT tokens on route changes
- Check token validity before allowing access to protected routes
- Redirect to login with return URL for unauthorized access
- Prevent access to guest-only pages when authenticated

### **JWT Component Integration**
**JWT Validation in Vue Components:**
- Email format validation for JWT authentication
- Password strength validation with security requirements
- Real-time form validation feedback

**JWT Authentication in Components:**
- Import and use Pinia authentication store
- Login function with JWT token handling
- Logout function with token blacklisting
- Reactive authentication state management
- User data access from JWT tokens

## 12. Testing Considerations

### **JWT Backend Testing**
- Unit tests for JWT token generation and validation
- Integration tests for JWT authentication views
- Permission system testing with JWT tokens
- JWT decorator functionality testing
- Token blacklisting and refresh testing

### **JWT Frontend Testing**
- Component testing for JWT auth forms
- Integration testing for JWT auth flows
- E2E testing for complete JWT user journeys
- Token lifecycle testing (refresh, expiry, blacklisting)
- Route guard testing with JWT authentication

### **JWT Test Suite**
Comprehensive test coverage includes:
- **Registration Flow**: JWT token generation on signup
- **Login Flow**: JWT authentication and token retrieval
- **Token Refresh**: Automatic token refresh mechanism
- **Permission Checks**: JWT-based authorization
- **Security Tests**: Invalid credentials, token blacklisting
- **Error Handling**: Network failures, token expiry scenarios

## 13. Future Enhancements

### **Immediate JWT Enhancements**
1. **Production Security**: 
   - HttpOnly cookies for token storage (instead of localStorage)
   - Secure token transmission (HTTPS only)
   - JWT signing key rotation
2. **Enhanced Token Management**:
   - Sliding session extension
   - Multiple device token management
   - Token usage analytics

### **Future JWT Improvements**
1. **Advanced Authentication**:
   - **Two-Factor Authentication (2FA)** with JWT
   - **Social Login Integration** (Google, Facebook) with JWT
   - **Biometric Authentication** for mobile JWT apps
2. **Security Enhancements**:
   - **JWT Refresh Token Rotation** (already implemented)
   - **Device Fingerprinting** for JWT security
   - **Geolocation-based Access Control**
3. **Mobile & API Features**:
   - **Mobile App JWT Integration**
   - **API Rate Limiting** by JWT user
   - **JWT Webhook Authentication** for external services
4. **Monitoring & Analytics**:
   - **JWT Token Usage Analytics**
   - **Authentication Event Logging**
   - **Security Incident Detection**

### **JWT Migration Benefits Achieved**
✅ **Stateless Authentication**: No server-side session storage required
✅ **Scalability**: Better support for microservices and load balancing  
✅ **Mobile Ready**: JWT tokens work seamlessly with mobile applications
✅ **API Integration**: Perfect for third-party API integrations
✅ **Security**: Token-based security with automatic expiry and blacklisting
✅ **Performance**: Reduced server memory usage and database queries
✅ **Cross-Domain**: Better support for cross-origin requests

## 🚀 **JWT Implementation Summary**

This authentication system has been **successfully migrated from session-based to JWT authentication**, providing a robust, secure, and scalable foundation for the CampusLink platform. The JWT implementation supports multiple user roles with appropriate access controls and delivers a seamless user experience.

### **✅ Completed JWT Features:**
- **Stateless JWT Authentication** with access/refresh token pairs
- **Automatic Token Refresh** with transparent user experience
- **Secure Token Blacklisting** for proper logout functionality
- **Role-based Authorization** using JWT claims
- **Frontend Token Management** with automatic retry logic
- **Comprehensive Security** with token expiry and validation
- **Mobile-Ready API** supporting cross-platform applications

### **🔐 Security Features:**
- Access tokens expire in 5 minutes (short-lived for security)
- Refresh tokens expire in 7 days with automatic rotation
- Token blacklisting prevents reuse of logged-out tokens
- Bearer token authentication with proper headers
- Automatic token refresh prevents user disruption
- Input validation and permission checks remain intact

### **📱 Benefits Achieved:**
- **Scalability**: Stateless authentication supports horizontal scaling
- **Performance**: Reduced server memory and database load
- **API-First**: Ready for mobile apps and third-party integrations  
- **Security**: Enhanced with modern JWT best practices
- **User Experience**: Seamless authentication with automatic token management

The JWT authentication migration is **complete, tested, and production-ready**! 🎉
