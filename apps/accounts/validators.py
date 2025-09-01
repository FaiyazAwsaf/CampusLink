import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

User = get_user_model()


class ValidationUtils:
    """Utility class for form validation"""
    
    @staticmethod
    def validate_email_format(email):
        """Validate email format and return cleaned email"""
        if not email:
            raise ValidationError("Email is required")
        
        email = email.strip().lower()
        
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Please enter a valid email address")
        
        # Additional email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError("Please enter a valid email address")
        
        return email
    
    @staticmethod
    def validate_email_unique(email, exclude_user_id=None):
        """Check if email is unique"""
        email = ValidationUtils.validate_email_format(email)
        
        # Check if email already exists
        user_query = User.objects.filter(email=email)
        if exclude_user_id:
            user_query = user_query.exclude(id=exclude_user_id)
        
        if user_query.exists():
            raise ValidationError("A user with this email already exists")
        
        return email
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password:
            raise ValidationError("Password is required")
        
        errors = []
        
        # Minimum length check
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        # Maximum length check
        if len(password) > 128:
            errors.append("Password must be less than 128 characters long")
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)")
        
        # Check for common weak passwords
        weak_passwords = [
            'password', '12345678', 'qwerty', 'abc123', 
            'password123', '123456789', 'admin', 'user'
        ]
        if password.lower() in weak_passwords:
            errors.append("Password is too common. Please choose a stronger password")
        
        if errors:
            raise ValidationError(errors)
        
        return password
    
    @staticmethod
    def validate_name(name):
        """Validate full name"""
        if not name:
            raise ValidationError("Name is required")
        
        name = name.strip()
        
        # Length validation
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        
        if len(name) > 255:
            raise ValidationError("Name must be less than 255 characters long")
        
        # Character validation
        if not re.match(r'^[a-zA-Z\s.]+$', name):
            raise ValidationError("Name can only contain letters, spaces, and dots")
        
        # Check for consecutive spaces
        if '  ' in name:
            raise ValidationError("Name cannot contain consecutive spaces")
        
        # Check for leading/trailing dots
        if name.startswith('.') or name.endswith('.'):
            raise ValidationError("Name cannot start or end with a dot")
        
        return name
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        if not phone:
            return None  # Phone is optional
        
        # Remove spaces and dashes
        phone_clean = re.sub(r'[\s-]', '', phone.strip())
        
        # Validate Bangladesh phone number format
        if not re.match(r'^(\+88)?01[0-9]{9}$', phone_clean):
            raise ValidationError(
                "Phone number must be in the format: +8801XXXXXXXXX or 01XXXXXXXXX"
            )
        
        return phone_clean
    
    @staticmethod
    def validate_image(image):
        """Validate uploaded image"""
        if not image:
            return None  # Image is optional
        
        # Check file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if image.size > max_size:
            raise ValidationError("Image file size cannot exceed 5MB")
        
        # Check file extension
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        file_extension = image.name.lower().split('.')[-1]
        if f'.{file_extension}' not in allowed_extensions:
            raise ValidationError(
                "Only JPG, JPEG, PNG, and GIF image files are allowed"
            )
        
        return image
    
    @staticmethod
    def validate_registration_data(data):
        """Validate complete registration data"""
        validated_data = {}
        errors = {}
        
        # Validate email
        try:
            validated_data['email'] = ValidationUtils.validate_email_unique(
                data.get('email', '')
            )
        except ValidationError as e:
            errors['email'] = e.messages if hasattr(e, 'messages') else [str(e)]

        # Validate password
        try:
            validated_data['password'] = ValidationUtils.validate_password(
                data.get('password', '')
            )
        except ValidationError as e:
            errors['password'] = e.messages if hasattr(e, 'messages') else [str(e)]

        # Validate name
        try:
            validated_data['name'] = ValidationUtils.validate_name(
                data.get('name', '')
            )
        except ValidationError as e:
            errors['name'] = e.messages if hasattr(e, 'messages') else [str(e)]

        # Validate phone (optional)
        try:
            phone = ValidationUtils.validate_phone(data.get('phone', ''))
            if phone:
                validated_data['phone'] = phone
        except ValidationError as e:
            errors['phone'] = e.messages if hasattr(e, 'messages') else [str(e)]

        # Validate image (optional)
        try:
            image = ValidationUtils.validate_image(data.get('image'))
            if image:
                validated_data['image'] = image
        except ValidationError as e:
            errors['image'] = e.messages if hasattr(e, 'messages') else [str(e)]

        # Handle entrepreneur flag (optional, defaults to False)
        validated_data['is_entrepreneur'] = bool(data.get('is_entrepreneur', False))

        if errors:
            raise ValidationError(errors)

        return validated_data
    
    @staticmethod
    def validate_login_data(data):
        """Validate login data"""
        validated_data = {}
        errors = {}
        
        # Validate email
        try:
            validated_data['email'] = ValidationUtils.validate_email_format(
                data.get('email', '')
            )
        except ValidationError as e:
            errors['email'] = str(e)
        
        # Validate password (basic check for login)
        password = data.get('password', '').strip()
        if not password:
            errors['password'] = "Password is required"
        else:
            validated_data['password'] = password
        
        if errors:
            raise ValidationError(errors)
        
        return validated_data
