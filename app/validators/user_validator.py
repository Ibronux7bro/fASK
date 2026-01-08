from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator, ValidationError
from app.models.user import User


class UserValidator(BaseValidator):
    """Validator for User model - separate from ORM validations"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user creation data"""
        validated_data = {}
        
        # Name validation
        if 'name' in data:
            validated_data['name'] = BaseValidator.required(
                BaseValidator.max_length(data['name'], 120, 'name'), 'name'
            )
        
        # Email validation
        if 'email' in data:
            email = BaseValidator.required(
                BaseValidator.max_length(data['email'], 120, 'email'), 'email'
            )
            validated_data['email'] = BaseValidator.email_format(email, 'email')
            validated_data['email'] = BaseValidator.validate_unique(
                validated_data['email'], User, 'email'
            )
        
        # Password validation
        if 'password' in data:
            validated_data['password'] = BaseValidator.required(
                BaseValidator.password_strength(data['password'], 'password'), 'password'
            )
        
        # Status validation
        if 'status' in data:
            validated_data['status'] = BaseValidator.boolean(data['status'], 'status')
        
        # Role ID validation
        if 'role_id' in data:
            validated_data['role_id'] = BaseValidator.required(
                BaseValidator.numeric(data['role_id'], 'role_id'), 'role_id'
            )
            validated_data['role_id'] = BaseValidator.positive_number(
                validated_data['role_id'], 'role_id'
            )
        
        return validated_data

    @staticmethod
    def validate_login(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate login data (email/password only)."""
        validated_data = {}

        if 'email' in data:
            email = BaseValidator.required(
                BaseValidator.max_length(data['email'], 120, 'email'),
                'email'
            )
            validated_data['email'] = BaseValidator.email_format(email, 'email')

        if 'password' in data:
            validated_data['password'] = BaseValidator.required(data['password'], 'password')

        return validated_data
    
    @staticmethod
    def validate_update(data: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        """Validate user update data"""
        validated_data = {}
        
        # Name validation (optional for update)
        if 'name' in data and data['name'] is not None:
            validated_data['name'] = BaseValidator.max_length(data['name'], 120, 'name')
        
        # Email validation (optional for update)
        if 'email' in data and data['email'] is not None:
            email = BaseValidator.max_length(data['email'], 120, 'email')
            validated_data['email'] = BaseValidator.email_format(email, 'email')
            validated_data['email'] = BaseValidator.validate_unique(
                validated_data['email'], User, 'email', exclude_id=user_id
            )
        
        # Password validation (optional for update)
        if 'password' in data and data['password'] is not None:
            validated_data['password'] = BaseValidator.password_strength(data['password'], 'password')
        
        # Status validation (optional for update)
        if 'status' in data and data['status'] is not None:
            validated_data['status'] = BaseValidator.boolean(data['status'], 'status')
        
        # Role ID validation (optional for update)
        if 'role_id' in data and data['role_id'] is not None:
            role_id = BaseValidator.numeric(data['role_id'], 'role_id')
            validated_data['role_id'] = BaseValidator.positive_number(role_id, 'role_id')
        
        return validated_data
