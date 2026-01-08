import re
from typing import Any, Dict, List, Optional, Union


class ValidationError(Exception):
    """Custom validation exception"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class BaseValidator:
    """Base validation class with common validation methods"""
    
    @staticmethod
    def required(value: Any, field_name: str) -> Any:
        """Check if value is not None or empty"""
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise ValidationError(field_name, f"{field_name} is required")
        return value
    
    @staticmethod
    def max_length(value: str, max_len: int, field_name: str) -> str:
        """Check string length"""
        if len(value) > max_len:
            raise ValidationError(field_name, f"{field_name} must be at most {max_len} characters")
        return value
    
    @staticmethod
    def min_length(value: str, min_len: int, field_name: str) -> str:
        """Check minimum string length"""
        if len(value) < min_len:
            raise ValidationError(field_name, f"{field_name} must be at least {min_len} characters")
        return value
    
    @staticmethod
    def email_format(value: str, field_name: str) -> str:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValidationError(field_name, f"{field_name} must be a valid email address")
        return value
    
    @staticmethod
    def password_strength(value: str, field_name: str) -> str:
        """Validate password strength - at least 8 chars, 1 uppercase, 1 lowercase, 1 number"""
        if len(value) < 8:
            raise ValidationError(field_name, f"{field_name} must be at least 8 characters")
        
        if not re.search(r'[A-Z]', value):
            raise ValidationError(field_name, f"{field_name} must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', value):
            raise ValidationError(field_name, f"{field_name} must contain at least one lowercase letter")
        
        if not re.search(r'\d', value):
            raise ValidationError(field_name, f"{field_name} must contain at least one number")
        
        return value
    
    @staticmethod
    def numeric(value: Any, field_name: str) -> Union[int, float]:
        """Check if value is numeric"""
        if not isinstance(value, (int, float)):
            try:
                return float(value)
            except (ValueError, TypeError):
                raise ValidationError(field_name, f"{field_name} must be a number")
        return value
    
    @staticmethod
    def positive_number(value: Union[int, float], field_name: str) -> Union[int, float]:
        """Check if number is positive"""
        if value <= 0:
            raise ValidationError(field_name, f"{field_name} must be a positive number")
        return value
    
    @staticmethod
    def non_negative(value: Union[int, float], field_name: str) -> Union[int, float]:
        """Check if number is non-negative"""
        if value < 0:
            raise ValidationError(field_name, f"{field_name} must be non-negative")
        return value
    
    @staticmethod
    def boolean(value: Any, field_name: str) -> bool:
        """Convert and validate boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value.lower() in ('true', '1', 'yes', 'on'):
                return True
            elif value.lower() in ('false', '0', 'no', 'off'):
                return False
        raise ValidationError(field_name, f"{field_name} must be a boolean value")
    
    @staticmethod
    def in_choices(value: Any, choices: List[Any], field_name: str) -> Any:
        """Check if value is in allowed choices"""
        if value not in choices:
            raise ValidationError(field_name, f"{field_name} must be one of: {', '.join(map(str, choices))}")
        return value
    
    @staticmethod
    def validate_unique(value: Any, model_class, field_name: str, exclude_id: Optional[int] = None) -> Any:
        """Check if value is unique in database (for email, username, etc.)"""
        query = model_class.query.filter(getattr(model_class, field_name) == value)
        if exclude_id:
            query = query.filter(model_class.id != exclude_id)
        
        if query.first():
            raise ValidationError(field_name, f"{field_name} already exists")
        return value
