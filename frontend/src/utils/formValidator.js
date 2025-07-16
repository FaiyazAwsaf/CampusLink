// Form validation utilities for the frontend
class FormValidator {
    
    static validateEmail(email) {
        const errors = [];
        
        if (!email) {
            errors.push('Email is required');
            return errors;
        }
        
        email = email.trim().toLowerCase();
        
        // Basic email regex
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailRegex.test(email)) {
            errors.push('Please enter a valid email address');
        }
        
        return errors;
    }
    
    static validatePassword(password) {
        const errors = [];
        
        if (!password) {
            errors.push('Password is required');
            return errors;
        }
        
        // Length check
        if (password.length < 8) {
            errors.push('Password must be at least 8 characters long');
        }
        
        if (password.length > 128) {
            errors.push('Password must be less than 128 characters long');
        }
        
        // Uppercase letter check
        if (!/[A-Z]/.test(password)) {
            errors.push('Password must contain at least one uppercase letter');
        }
        
        // Lowercase letter check
        if (!/[a-z]/.test(password)) {
            errors.push('Password must contain at least one lowercase letter');
        }
        
        // Number check
        if (!/\d/.test(password)) {
            errors.push('Password must contain at least one number');
        }
        
        // Special character check
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            errors.push('Password must contain at least one special character');
        }
        
        // Common password check
        const weakPasswords = [
            'password', '12345678', 'qwerty', 'abc123', 
            'password123', '123456789', 'admin', 'user'
        ];
        
        if (weakPasswords.includes(password.toLowerCase())) {
            errors.push('Password is too common. Please choose a stronger password');
        }
        
        return errors;
    }
    
    static validateName(name) {
        const errors = [];
        
        if (!name) {
            errors.push('Name is required');
            return errors;
        }
        
        name = name.trim();
        
        // Length check
        if (name.length < 2) {
            errors.push('Name must be at least 2 characters long');
        }
        
        if (name.length > 255) {
            errors.push('Name must be less than 255 characters long');
        }
        
        // Character check
        if (!/^[a-zA-Z\s.]+$/.test(name)) {
            errors.push('Name can only contain letters, spaces, and dots');
        }
        
        // Consecutive spaces check
        if (name.includes('  ')) {
            errors.push('Name cannot contain consecutive spaces');
        }
        
        // Leading/trailing dots check
        if (name.startsWith('.') || name.endsWith('.')) {
            errors.push('Name cannot start or end with a dot');
        }
        
        return errors;
    }
    
    static validatePhone(phone) {
        const errors = [];
        
        if (!phone) {
            return errors; // Phone is optional
        }
        
        // Remove spaces and dashes
        const phoneClean = phone.replace(/[\s-]/g, '');
        
        // Bangladesh phone number format
        const phoneRegex = /^(\+88)?01[0-9]{9}$/;
        if (!phoneRegex.test(phoneClean)) {
            errors.push('Phone number must be in the format: +8801XXXXXXXXX or 01XXXXXXXXX');
        }
        
        return errors;
    }
    
    static validateImage(file) {
        const errors = [];
        
        if (!file) {
            return errors; // Image is optional
        }
        
        // Check file size (max 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB in bytes
        if (file.size > maxSize) {
            errors.push('Image file size cannot exceed 5MB');
        }
        
        // Check file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            errors.push('Only JPG, JPEG, PNG, and GIF image files are allowed');
        }
        
        return errors;
    }
    
    static validateRegistrationForm(formData) {
        const errors = {};
        
        // Validate email
        const emailErrors = this.validateEmail(formData.email);
        if (emailErrors.length > 0) {
            errors.email = emailErrors;
        }
        
        // Validate password
        const passwordErrors = this.validatePassword(formData.password);
        if (passwordErrors.length > 0) {
            errors.password = passwordErrors;
        }
        
        // Validate name
        const nameErrors = this.validateName(formData.name);
        if (nameErrors.length > 0) {
            errors.name = nameErrors;
        }
        
        // Validate phone
        const phoneErrors = this.validatePhone(formData.phone);
        if (phoneErrors.length > 0) {
            errors.phone = phoneErrors;
        }
        
        // Validate image
        const imageErrors = this.validateImage(formData.image);
        if (imageErrors.length > 0) {
            errors.image = imageErrors;
        }
        
        return errors;
    }
    
    static validateLoginForm(formData) {
        const errors = {};
        
        // Validate email
        const emailErrors = this.validateEmail(formData.email);
        if (emailErrors.length > 0) {
            errors.email = emailErrors;
        }
        
        // Basic password validation for login
        if (!formData.password) {
            errors.password = ['Password is required'];
        }
        
        return errors;
    }
    
    static displayErrors(errors, errorContainer) {
        // Clear previous errors
        errorContainer.innerHTML = '';
        
        if (Object.keys(errors).length === 0) {
            return;
        }
        
        // Create error list
        const errorList = document.createElement('ul');
        errorList.className = 'error-list';
        
        for (const [field, fieldErrors] of Object.entries(errors)) {
            if (Array.isArray(fieldErrors)) {
                fieldErrors.forEach(error => {
                    const errorItem = document.createElement('li');
                    errorItem.className = 'error-item';
                    errorItem.textContent = error;
                    errorList.appendChild(errorItem);
                });
            } else {
                const errorItem = document.createElement('li');
                errorItem.className = 'error-item';
                errorItem.textContent = fieldErrors;
                errorList.appendChild(errorItem);
            }
        }
        
        errorContainer.appendChild(errorList);
    }
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FormValidator;
}
