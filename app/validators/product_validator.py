from typing import Dict, Any
from app.validators.base_validator import BaseValidator


class ProductValidator(BaseValidator):
    """Validator for Product model - separate from ORM validations"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate product creation data"""
        validated_data = {}
        
        # Name validation
        if 'name' in data:
            validated_data['name'] = BaseValidator.required(
                BaseValidator.max_length(data['name'], 120, 'name'), 'name'
            )
        
        # Price validation
        if 'price' in data:
            price = BaseValidator.required(
                BaseValidator.numeric(data['price'], 'price'), 'price'
            )
            validated_data['price'] = BaseValidator.positive_number(price, 'price')
        
        # Quantity validation
        if 'quantity' in data:
            quantity = BaseValidator.required(
                BaseValidator.numeric(data['quantity'], 'quantity'), 'quantity'
            )
            validated_data['quantity'] = BaseValidator.non_negative(quantity, 'quantity')
        
        # Description validation (optional)
        if 'description' in data and data['description'] is not None:
            validated_data['description'] = data['description']
        
        return validated_data
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate product update data"""
        validated_data = {}
        
        # Name validation (optional for update)
        if 'name' in data and data['name'] is not None:
            validated_data['name'] = BaseValidator.max_length(data['name'], 120, 'name')
        
        # Price validation (optional for update)
        if 'price' in data and data['price'] is not None:
            price = BaseValidator.numeric(data['price'], 'price')
            validated_data['price'] = BaseValidator.positive_number(price, 'price')
        
        # Quantity validation (optional for update)
        if 'quantity' in data and data['quantity'] is not None:
            quantity = BaseValidator.numeric(data['quantity'], 'quantity')
            validated_data['quantity'] = BaseValidator.non_negative(quantity, 'quantity')
        
        # Description validation (optional)
        if 'description' in data and data['description'] is not None:
            validated_data['description'] = data['description']
        
        return validated_data
