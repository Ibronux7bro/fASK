from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from app.models.invoice import Invoice
from app.models.invoice_product import InvoiceProduct
from app.models.customer import Customer
from app.validators.invoice_validator import InvoiceValidator, InvoiceProductValidator
from app.validators.product_validator import ProductValidator
from app.validators.customer_validator import CustomerValidator
from app.middleware.auth_middleware import permission_required
from app.services.invoice_service import InvoiceService
from app import db

invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/products', methods=['GET'])
@permission_required('Product', 'read')
def get_products():
    """Get all products with prices"""
    try:
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'quantity': p.quantity,
            'description': p.description
        } for p in products]), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get products', 'error': str(e)}), 400

@invoice_bp.route('/products', methods=['POST'])
@permission_required('Product', 'create')
def create_product():
    """Create new product"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Handle quantity/stock_quantity mismatch
        if 'stock_quantity' in data and 'quantity' not in data:
            data['quantity'] = data.pop('stock_quantity')
            
        validated_data = ProductValidator.validate_create(data)
        
        product = Product(**validated_data)
        product.created_by = current_user_id
        product.updated_by = current_user_id
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': product.quantity
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create product', 'error': str(e)}), 400

@invoice_bp.route('/products/<int:product_id>', methods=['GET'])
@permission_required('Product', 'read')
def get_product(product_id):
    """Get single product"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'quantity': product.quantity
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get product', 'error': str(e)}), 400

@invoice_bp.route('/products/<int:product_id>', methods=['PUT'])
@permission_required('Product', 'update')
def update_product(product_id):
    """Update product"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Handle quantity/stock_quantity mismatch
        if 'stock_quantity' in data and 'quantity' not in data:
            data['quantity'] = data.pop('stock_quantity')
            
        validated_data = ProductValidator.validate_update(data)
        
        if 'name' in validated_data:
            product.name = validated_data['name']
        if 'description' in validated_data:
            product.description = validated_data['description']
        if 'price' in validated_data:
            product.price = validated_data['price']
        if 'quantity' in validated_data:
            product.quantity = validated_data['quantity']
            
        product.updated_by = current_user_id
        db.session.commit()
        
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update product', 'error': str(e)}), 400

@invoice_bp.route('/products/<int:product_id>', methods=['DELETE'])
@permission_required('Product', 'delete')
def delete_product(product_id):
    """Delete product"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Check if product is used in any invoice items (optional integrity check)
        # For now, just delete
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete product', 'error': str(e)}), 400

@invoice_bp.route('/customers', methods=['GET'])
@permission_required('Customer', 'read')
def get_customers():
    """Get all customers"""
    try:
        customers = Customer.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'email': c.email,
            'phone': c.phone,
            'mobile': c.mobile
        } for c in customers]), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get customers', 'error': str(e)}), 400

@invoice_bp.route('/customers', methods=['POST'])
@permission_required('Customer', 'create')
def create_customer():
    """Create new customer"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        validated_data = CustomerValidator.validate_create(data)
        
        customer = Customer(**validated_data)
        customer.created_by = current_user_id
        customer.updated_by = current_user_id
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'message': 'Customer created successfully',
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create customer', 'error': str(e)}), 400

@invoice_bp.route('/customers/<int:customer_id>', methods=['GET'])
@permission_required('Customer', 'read')
def get_customer(customer_id):
    """Get single customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'mobile': customer.mobile
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get customer', 'error': str(e)}), 400

@invoice_bp.route('/customers/<int:customer_id>', methods=['PUT'])
@permission_required('Customer', 'update')
def update_customer(customer_id):
    """Update customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        validated_data = CustomerValidator.validate_update(data, customer_id)
        
        if 'name' in validated_data:
            customer.name = validated_data['name']
        if 'email' in validated_data:
            customer.email = validated_data['email']
        if 'phone' in validated_data:
            customer.phone = validated_data['phone']
        if 'address' in validated_data:
            customer.address = validated_data['address']
        if 'mobile' in validated_data:
            customer.mobile = validated_data['mobile']
            
        customer.updated_by = current_user_id
        db.session.commit()
        
        return jsonify({'message': 'Customer updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update customer', 'error': str(e)}), 400

@invoice_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
@permission_required('Customer', 'delete')
def delete_customer(customer_id):
    """Delete customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        
        # Optional: check dependencies (invoices)
        # For now, just delete
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete customer', 'error': str(e)}), 400

@invoice_bp.route('/invoices', methods=['GET'])
@permission_required('Invoice', 'read')
def get_invoices():
    """Get all invoices - filtered by role hierarchy"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get invoices based on role hierarchy
        invoices = InvoiceService.get_accessible_invoices(current_user_id)
        
        return jsonify([{
            'id': inv.id,
            'customer_name': inv.customer.name if inv.customer else 'N/A',
            'total_amount': float(inv.total_amount),
            'status': inv.status,
            'invoice_date': inv.invoice_date.strftime('%Y-%m-%d') if inv.invoice_date else None
        } for inv in invoices]), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get invoices', 'error': str(e)}), 400

@invoice_bp.route('/invoices', methods=['POST'])
@permission_required('Invoice', 'create')
def create_invoice():
    """Create new invoice with items"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Validate invoice data
        invoice_data = InvoiceValidator.validate_create(data)
        
        # Check inventory availability before creating invoice
        if 'items' in data:
            is_available, error_msg = InvoiceService.validate_inventory_availability(data['items'])
            if not is_available:
                return jsonify({'message': error_msg}), 400
        
        # Create invoice
        invoice = Invoice(**invoice_data)
        invoice.created_by = current_user_id
        db.session.add(invoice)
        db.session.flush()  # Get invoice ID
        
        # Add invoice items if provided
        if 'items' in data:
            total_amount = 0
            for item_data in data['items']:
                item_data['invoice_id'] = invoice.id
                validated_item = InvoiceProductValidator.validate_create(item_data)
                
                invoice_product = InvoiceProduct(**validated_item)
                db.session.add(invoice_product)
                total_amount += invoice_product.amount
            
            invoice.total_amount = total_amount
            
            # Decrease inventory after successful invoice creation
            is_decreased, error_msg = InvoiceService.decrease_inventory(data['items'])
            if not is_decreased:
                db.session.rollback()
                return jsonify({'message': f'Failed to update inventory: {error_msg}'}), 500
        
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice created successfully',
            'invoice_id': invoice.id,
            'total_amount': float(invoice.total_amount)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create invoice', 'error': str(e)}), 400

@invoice_bp.route('/invoices/<int:invoice_id>/items')
@permission_required('Invoice', 'read')
def get_invoice_items(invoice_id):
    """Get invoice items"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        items = InvoiceProduct.query.filter_by(invoice_id=invoice.id).all()
        
        items_data = []
        for item in items:
            items_data.append({
                'product_name': item.product.name if item.product else 'N/A',
                'price': float(item.product.price) if item.product else 0,
                'quantity': item.quantity,
                'amount': float(item.amount)
            })
        
        return jsonify({
            'items': items_data,
            'invoice_id': invoice_id,
            'total_amount': float(invoice.total_amount),
            'date': invoice.invoice_date.strftime('%Y-%m-%d') if invoice.invoice_date else 'N/A',
            'customer': invoice.customer.name if invoice.customer else 'N/A',
            'status': invoice.status
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get invoice items', 'error': str(e)}), 400


@invoice_bp.route('/invoices/<int:invoice_id>/status', methods=['PUT'])
@jwt_required()
def update_invoice_status(invoice_id):
    """Update invoice status - Admin and Sales Manager only"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'message': 'Status is required'}), 400
        
        # Check if user can change invoice status
        if not InvoiceService.can_change_invoice_status(current_user_id):
            return jsonify({'message': 'Only Admin and Sales Manager can change invoice status'}), 403
        
        # Get invoice
        invoice = Invoice.query.get_or_404(invoice_id)
        
        # Check if user can access this invoice
        if not InvoiceService.can_access_invoice(current_user_id, invoice_id):
            return jsonify({'message': 'Access denied to this invoice'}), 403
        
        # Validate status transition
        if not InvoiceService.validate_status_transition(invoice.status, new_status):
            return jsonify({
                'message': f'Invalid status transition from {invoice.status} to {new_status}',
                'valid_transitions': {
                    'pending': ['paid', 'cancelled'],
                    'paid': [],
                    'cancelled': []
                }
            }), 400
        
        # Update status
        old_status = invoice.status
        invoice.status = new_status
        invoice.updated_by = current_user_id
        
        # If cancelling invoice, restore inventory
        if new_status == 'cancelled':
            is_restored, error_msg = InvoiceService.restore_inventory(invoice_id)
            if not is_restored:
                db.session.rollback()
                return jsonify({'message': f'Failed to restore inventory: {error_msg}'}), 500
        
        db.session.commit()
        
        return jsonify({
            'message': f'Invoice status updated from {old_status} to {new_status}',
            'invoice_id': invoice_id,
            'old_status': old_status,
            'new_status': new_status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update invoice status', 'error': str(e)}), 400

@invoice_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
@permission_required('Invoice', 'read')
def get_invoice(invoice_id):
    """Get single invoice with items"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user can access this invoice
        if not InvoiceService.can_access_invoice(current_user_id, invoice_id):
            return jsonify({'message': 'Access denied to this invoice'}), 403
        
        # Get invoice
        invoice = Invoice.query.get_or_404(invoice_id)
        
        # Get items
        items = InvoiceProduct.query.filter_by(invoice_id=invoice.id).all()
        
        items_data = []
        for item in items:
            items_data.append({
                'product_name': item.product.name if item.product else 'N/A',
                'product_id': item.product_id,
                'price': float(item.product.price) if item.product else 0,
                'quantity': item.quantity,
                'amount': float(item.amount)
            })
        
        return jsonify({
            'id': invoice.id,
            'customer_name': invoice.customer.name if invoice.customer else 'N/A',
            'customer_id': invoice.customer_id,
            'total_amount': float(invoice.total_amount),
            'status': invoice.status,
            'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d') if invoice.invoice_date else None,
            'items': items_data
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get invoice', 'error': str(e)}), 400

@invoice_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
@permission_required('Invoice', 'update')
def update_invoice(invoice_id):
    """Update invoice"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get invoice
        invoice = Invoice.query.get_or_404(invoice_id)
        
        # Check if user can access this invoice
        if not InvoiceService.can_access_invoice(current_user_id, invoice_id):
            return jsonify({'message': 'Access denied to this invoice'}), 403
        
        # Update allowed fields
        if 'customer_id' in data:
            invoice.customer_id = data['customer_id']
        
        if 'invoice_date' in data:
            invoice.invoice_date = data['invoice_date']
        
        # Handle status change
        if 'status' in data:
            new_status = data['status']
            
            # Check if user can change invoice status
            if not InvoiceService.can_change_invoice_status(current_user_id):
                return jsonify({'message': 'Only Admin and Sales Manager can change invoice status'}), 403
            
            # Validate status transition
            if not InvoiceService.validate_status_transition(invoice.status, new_status):
                return jsonify({'message': f'Invalid status transition from {invoice.status} to {new_status}'}), 400
            
            invoice.status = new_status
        
        invoice.updated_by = current_user_id
        db.session.commit()
        
        return jsonify({'message': 'Invoice updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update invoice', 'error': str(e)}), 400

@invoice_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
@permission_required('Invoice', 'delete')
def delete_invoice(invoice_id):
    """Delete invoice"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get invoice
        invoice = Invoice.query.get_or_404(invoice_id)
        
        # Check if user can access this invoice
        if not InvoiceService.can_access_invoice(current_user_id, invoice_id):
            return jsonify({'message': 'Access denied to this invoice'}), 403
        
        # Delete invoice items first
        InvoiceProduct.query.filter_by(invoice_id=invoice.id).delete()
        
        # Delete invoice
        db.session.delete(invoice)
        db.session.commit()
        
        return jsonify({'message': 'Invoice deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete invoice', 'error': str(e)}), 400
