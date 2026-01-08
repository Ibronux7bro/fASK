from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator, ValidationError
from app.models.customer import Customer


class CustomerValidator(BaseValidator):
    """Validator for Customer model - separate from ORM validations"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate customer creation data"""
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
                validated_data['email'], Customer, 'email'
            )
        
        # Address validation (optional)
        if 'address' in data and data['address'] is not None:
            validated_data['address'] = BaseValidator.max_length(data['address'], 255, 'address')
        
        # Phone validation (optional)
        if 'phone' in data and data['phone'] is not None:
            validated_data['phone'] = BaseValidator.max_length(data['phone'], 20, 'phone')
        
        # Mobile validation (optional)
        if 'mobile' in data and data['mobile'] is not None:
            validated_data['mobile'] = BaseValidator.max_length(data['mobile'], 20, 'mobile')
        
        return validated_data
    
    @staticmethod
    def validate_update(data: Dict[str, Any], customer_id: int) -> Dict[str, Any]:
        """Validate customer update data"""
        validated_data = {}
        
        # Name validation (optional for update)
        if 'name' in data and data['name'] is not None:
            validated_data['name'] = BaseValidator.max_length(data['name'], 120, 'name')
        
        # Email validation (optional for update)
        if 'email' in data and data['email'] is not None:
            email = BaseValidator.max_length(data['email'], 120, 'email')
            validated_data['email'] = BaseValidator.email_format(email, 'email')
            validated_data['email'] = BaseValidator.validate_unique(
                validated_data['email'], Customer, 'email', exclude_id=customer_id
            )
        
        # Address validation (optional)
        if 'address' in data and data['address'] is not None:
            validated_data['address'] = BaseValidator.max_length(data['address'], 255, 'address')
        
        # Phone validation (optional)
        if 'phone' in data and data['phone'] is not None:
            validated_data['phone'] = BaseValidator.max_length(data['phone'], 20, 'phone')
        
        # Mobile validation (optional)
        if 'mobile' in data and data['mobile'] is not None:
            validated_data['mobile'] = BaseValidator.max_length(data['mobile'], 20, 'mobile')
        
        return validated_data
