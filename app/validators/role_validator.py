from typing import Dict, Any, Optional
from app.validators.base_validator import BaseValidator, ValidationError
from app.models.role import Role


class RoleValidator(BaseValidator):
    """Validator for Role model - separate from ORM validations"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate role creation data"""
        validated_data = {}
        
        # Name validation
        if 'name' in data:
            validated_data['name'] = BaseValidator.required(
                BaseValidator.max_length(data['name'], 100, 'name'), 'name'
            )
            # Check for unique role name
            validated_data['name'] = BaseValidator.validate_unique(
                validated_data['name'], Role, 'name'
            )
        
        # Status validation
        if 'status' in data:
            validated_data['status'] = BaseValidator.boolean(data['status'], 'status')
        
        # parent_role_id is assigned by backend based on role name - not from request
        
        return validated_data
    
    @staticmethod
    def validate_update(data: Dict[str, Any], role_id: int) -> Dict[str, Any]:
        """Validate role update data"""
        validated_data = {}
        
        # Name validation (optional for update)
        if 'name' in data and data['name'] is not None:
            validated_data['name'] = BaseValidator.max_length(data['name'], 100, 'name')
            # Check for unique role name (excluding current role)
            validated_data['name'] = BaseValidator.validate_unique(
                validated_data['name'], Role, 'name', exclude_id=role_id
            )
        
        # Status validation (optional for update)
        if 'status' in data and data['status'] is not None:
            validated_data['status'] = BaseValidator.boolean(data['status'], 'status')
        
        # parent_role_id cannot be updated - assigned by backend only
        
        return validated_data


class PermissionValidator(BaseValidator):
    """Validator for Permission model - separate from ORM validations"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate permission creation data"""
        validated_data = {}
        
        # Role ID validation
        if 'role_id' in data:
            role_id = BaseValidator.required(
                BaseValidator.numeric(data['role_id'], 'role_id'), 'role_id'
            )
            validated_data['role_id'] = BaseValidator.positive_number(role_id, 'role_id')
        
        # Model name validation
        if 'model_name' in data:
            validated_data['model_name'] = BaseValidator.required(
                BaseValidator.max_length(data['model_name'], 100, 'model_name'), 'model_name'
            )
        
        # CRUD permissions validation
        crud_fields = ['can_create', 'can_read', 'can_update', 'can_delete']
        for field in crud_fields:
            if field in data:
                validated_data[field] = BaseValidator.boolean(data[field], field)
        
        return validated_data
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate permission update data"""
        validated_data = {}
        
        # CRUD permissions validation (optional for update)
        crud_fields = ['can_create', 'can_read', 'can_update', 'can_delete']
        for field in crud_fields:
            if field in data and data[field] is not None:
                validated_data[field] = BaseValidator.boolean(data[field], field)
        
        return validated_data
