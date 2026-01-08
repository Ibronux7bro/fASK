from typing import Dict, Any, List, Optional
from flask import jsonify
from app.models.invoice import Invoice
from app.models.invoice_product import InvoiceProduct
from app.models.product import Product
from app.models.user import User
from app.models.role import Role
from app.services.role_service import RoleService
from app import db


class InvoiceService:
    """Service layer for invoice business logic"""
    
    @staticmethod
    def can_access_invoice(user_id: int, invoice_id: int) -> bool:
        """Check if user can access invoice (own record or child role's record)"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return False
        
        # Admin can access all invoices
        if user.role.name == 'Admin':
            return True
        
        # Can access own invoices
        if invoice.created_by == user_id:
            return True
        
        # Can access invoices created by child roles
        child_role_ids = RoleService.get_child_role_ids(user.role_id)
        
        # Get creator of invoice
        creator = User.query.get(invoice.created_by)
        if creator and creator.role_id in child_role_ids:
            return True
        
        return False
    
    @staticmethod
    def get_accessible_invoices(user_id: int) -> List[Invoice]:
        """Get invoices that user can access"""
        user = User.query.get(user_id)
        if not user:
            return []
        
        # Admin can see all invoices
        if user.role.name == 'Admin':
            return Invoice.query.all()
        
        # Get child role IDs
        child_role_ids = RoleService.get_child_role_ids(user.role_id)
        child_role_ids.append(user.role_id)  # Include own role
        
        # Get users in child roles
        child_users = User.query.filter(User.role_id.in_(child_role_ids)).all()
        child_user_ids = [u.id for u in child_users]
        
        # Get invoices created by these users
        return Invoice.query.filter(Invoice.created_by.in_(child_user_ids)).all()
    
    @staticmethod
    def can_change_invoice_status(user_id: int) -> bool:
        """Check if user can change invoice status (Admin or Sales Manager only)"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        return user.role.name in ['Admin', 'Sales Manager']
    
    @staticmethod
    def validate_status_transition(current_status: str, new_status: str) -> bool:
        """Validate invoice status transition"""
        valid_transitions = {
            'pending': ['paid', 'cancelled'],
            'paid': [],  # Paid invoices cannot be changed
            'cancelled': []  # Cancelled invoices cannot be changed
        }
        
        return new_status in valid_transitions.get(current_status, [])
    
    @staticmethod
    def validate_inventory_availability(items: List[Dict[str, Any]]) -> tuple[bool, str]:
        """Validate if products have sufficient inventory"""
        for item in items:
            product = Product.query.get(item.get('product_id'))
            if not product:
                return False, f"Product {item.get('product_id')} not found"
            
            if product.quantity < item.get('quantity', 0):
                return False, f"Insufficient stock for {product.name}. Available: {product.quantity}, Requested: {item.get('quantity', 0)}"
        
        return True, ""
    
    @staticmethod
    def decrease_inventory(items: List[Dict[str, Any]]) -> tuple[bool, str]:
        """Decrease product quantities after invoice creation"""
        try:
            for item in items:
                product = Product.query.get(item.get('product_id'))
                if product:
                    product.quantity -= item.get('quantity', 0)
                    db.session.add(product)
            
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def restore_inventory(invoice_id: int) -> tuple[bool, str]:
        """Restore inventory when invoice is cancelled"""
        try:
            invoice_items = InvoiceProduct.query.filter_by(invoice_id=invoice_id).all()
            
            for item in invoice_items:
                product = Product.query.get(item.product_id)
                if product:
                    product.quantity += item.quantity
                    db.session.add(product)
            
            db.session.commit()
            return True, ""
        except Exception as e:
            db.session.rollback()
            return False, str(e)
