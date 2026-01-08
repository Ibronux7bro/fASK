from typing import Dict, Any
from app.validators.base_validator import BaseValidator
from datetime import datetime


class InvoiceValidator(BaseValidator):
    """Validator for Invoice model - separate from ORM validations"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate invoice creation data"""
        validated_data = {}
        
        # Customer ID validation
        if 'customer_id' in data:
            customer_id = BaseValidator.required(
                BaseValidator.numeric(data['customer_id'], 'customer_id'), 'customer_id'
            )
            validated_data['customer_id'] = BaseValidator.positive_number(customer_id, 'customer_id')
        
        # Invoice date validation (optional, defaults to current date)
        if 'invoice_date' in data and data['invoice_date'] is not None:
            validated_data['invoice_date'] = data['invoice_date']
        
        # Total amount validation (optional, defaults to 0)
        if 'total_amount' in data and data['total_amount'] is not None:
            total_amount = BaseValidator.numeric(data['total_amount'], 'total_amount')
            validated_data['total_amount'] = BaseValidator.non_negative(total_amount, 'total_amount')
        
        # Status validation (optional, defaults to 'pending')
        if 'status' in data and data['status'] is not None:
            validated_data['status'] = BaseValidator.in_choices(
                data['status'], ['pending', 'paid', 'cancelled'], 'status'
            )
        else:
            # Auto-set status to pending for new invoices
            validated_data['status'] = 'pending'
        
        return validated_data
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate invoice update data"""
        validated_data = {}
        
        # Customer ID validation (optional for update)
        if 'customer_id' in data and data['customer_id'] is not None:
            customer_id = BaseValidator.numeric(data['customer_id'], 'customer_id')
            validated_data['customer_id'] = BaseValidator.positive_number(customer_id, 'customer_id')
        
        # Invoice date validation (optional)
        if 'invoice_date' in data and data['invoice_date'] is not None:
            validated_data['invoice_date'] = data['invoice_date']
        
        # Total amount validation (optional)
        if 'total_amount' in data and data['total_amount'] is not None:
            total_amount = BaseValidator.numeric(data['total_amount'], 'total_amount')
            validated_data['total_amount'] = BaseValidator.non_negative(total_amount, 'total_amount')
        
        # Status validation (optional)
        if 'status' in data and data['status'] is not None:
            validated_data['status'] = BaseValidator.in_choices(
                data['status'], ['pending', 'paid', 'cancelled'], 'status'
            )
        
        return validated_data


class InvoiceProductValidator(BaseValidator):
    """Validator for InvoiceProduct model - separate from ORM validations"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate invoice product creation data"""
        validated_data = {}
        
        # Invoice ID validation
        if 'invoice_id' in data:
            invoice_id = BaseValidator.required(
                BaseValidator.numeric(data['invoice_id'], 'invoice_id'), 'invoice_id'
            )
            validated_data['invoice_id'] = BaseValidator.positive_number(invoice_id, 'invoice_id')
        
        # Product ID validation
        if 'product_id' in data:
            product_id = BaseValidator.required(
                BaseValidator.numeric(data['product_id'], 'product_id'), 'product_id'
            )
            validated_data['product_id'] = BaseValidator.positive_number(product_id, 'product_id')
        
        # Quantity validation
        if 'quantity' in data:
            quantity = BaseValidator.required(
                BaseValidator.numeric(data['quantity'], 'quantity'), 'quantity'
            )
            validated_data['quantity'] = BaseValidator.positive_number(quantity, 'quantity')
        
        # Amount validation
        if 'amount' in data:
            amount = BaseValidator.required(
                BaseValidator.numeric(data['amount'], 'amount'), 'amount'
            )
            validated_data['amount'] = BaseValidator.positive_number(amount, 'amount')
        
        return validated_data
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate invoice product update data"""
        validated_data = {}
        
        # Quantity validation (optional for update)
        if 'quantity' in data and data['quantity'] is not None:
            quantity = BaseValidator.numeric(data['quantity'], 'quantity')
            validated_data['quantity'] = BaseValidator.positive_number(quantity, 'quantity')
        
        # Amount validation (optional for update)
        if 'amount' in data and data['amount'] is not None:
            amount = BaseValidator.numeric(data['amount'], 'amount')
            validated_data['amount'] = BaseValidator.positive_number(amount, 'amount')
        
        return validated_data
