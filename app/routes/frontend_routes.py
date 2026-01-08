from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from datetime import datetime
from app import db
from app.models.invoice import Invoice
from app.models.invoice_product import InvoiceProduct
from app.models.product import Product
from app.models.customer import Customer
from app.models.user import User
from app.middleware.auth_middleware import permission_required
from app.services.invoice_service import InvoiceService

frontend_bp = Blueprint('frontend', __name__)

def get_current_user():
    """Get the current logged-in user from JWT token"""
    try:
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        return User.query.get(current_user_id)
    except:
        return None

@frontend_bp.route('/')
def home():
    return render_template('login.html')

@frontend_bp.route('/login')
def login_page():
    return render_template('login.html')

# ========================= CUSTOMER ROUTES =========================
@frontend_bp.route('/customers')
def customers_list():
    """Serve customers list page. Actual data is loaded via JS using protected API calls."""
    return render_template('customers/list.html')

@frontend_bp.route('/customers/create', methods=['GET'])
def create_customer():
    """Serve create customer page shell"""
    return render_template('customers/create.html')

@frontend_bp.route('/customers/edit/<int:customer_id>', methods=['GET'])
def edit_customer(customer_id):
    """Serve edit customer page shell - data loaded via JS"""
    # We pass the ID to the template so JS can use it
    return render_template('customers/edit.html', customer_id=customer_id)

@frontend_bp.route('/customers/view/<int:customer_id>')
def view_customer(customer_id):
    """Serve view customer page shell"""
    return render_template('customers/view.html', customer_id=customer_id)

# Delete handled via API


# ========================= PRODUCT ROUTES =========================
# ========================= PRODUCT ROUTES =========================
@frontend_bp.route('/products')
def products_list():
    """Serve products list page. Actual data is loaded via JS using protected API calls."""
    return render_template('products/list.html')

@frontend_bp.route('/products/create', methods=['GET'])
def create_product():
    return render_template('products/create.html')

@frontend_bp.route('/products/edit/<int:product_id>', methods=['GET'])
def edit_product(product_id):
    # We pass the ID to the template, JS will fetch details
    return render_template('products/edit.html', product_id=product_id)

@frontend_bp.route('/products/view/<int:product_id>')
def view_product(product_id):
    return render_template('products/view.html', product_id=product_id)

# Delete is handled via API, no HTML route needed usually, but if there was one:
# No delete route needed for frontend navigation as it's an action, not a page.

# ========================= INVOICE ROUTES =========================
@frontend_bp.route('/invoices')
def invoice_list():
    """Serve the invoice list page. Actual data is loaded via JS using protected API calls, so no JWT header is needed for this HTML response."""
    return render_template('invoices/list.html')

@frontend_bp.route('/invoices/view/<int:invoice_id>')
@jwt_required()
@permission_required('Invoice', 'read')
def view_invoice(invoice_id):
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('frontend.login_page'))
    
    # Check if user can access this invoice
    if not InvoiceService.can_access_invoice(current_user.id, invoice_id):
        flash('Access denied to this invoice', 'error')
        return redirect(url_for('frontend.invoice_list'))
    
    invoice = Invoice.query.get_or_404(invoice_id)
    items = InvoiceProduct.query.filter_by(invoice_id=invoice.id).all()
    return render_template('invoices/view.html', invoice=invoice, items=items)

@frontend_bp.route('/invoices/edit/<int:invoice_id>', methods=['GET', 'POST'])
@jwt_required()
@permission_required('Invoice', 'update')
def edit_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    customers = Customer.query.all()
    products = Product.query.all()
    
    # Convert products to serializable format
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': product.quantity,
            'description': product.description
        })
    
    if request.method == 'POST':
        # Check if user can change invoice status
        new_status = request.form.get('status')
        if new_status != invoice.status:
            if not InvoiceService.can_change_invoice_status():
                flash('Only Admin and Sales Manager can change invoice status', 'error')
                return render_template('invoices/edit.html', invoice=invoice, customers=customers, products=products_data)
            
            # Validate status transition
            if not InvoiceService.validate_status_transition(invoice.status, new_status):
                flash(f'Invalid status transition from {invoice.status} to {new_status}', 'error')
                return render_template('invoices/edit.html', invoice=invoice, customers=customers, products=products_data)

        invoice.customer_id = request.form.get('customer_id')
        invoice.status = new_status or invoice.status  # Only change status if provided and allowed
        invoice.invoice_date = request.form.get('invoice_date')
        
        # Get old items for inventory restoration
        old_items = InvoiceProduct.query.filter_by(invoice_id=invoice.id).all()
        old_quantities = {}
        for item in old_items:
            old_quantities[item.product_id] = item.quantity
        
        # Update invoice items
        InvoiceProduct.query.filter_by(invoice_id=invoice.id).delete()
        
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        
        # Validate inventory availability
        new_items = []
        total_amount = 0
        for i in range(len(product_ids)):
            if product_ids[i]:
                product = Product.query.get(product_ids[i])
                qty = int(quantities[i])
                amount = product.price * qty
                total_amount += amount
                
                new_items.append({
                    'product_id': product.id,
                    'quantity': qty
                })
                
                item = InvoiceProduct(
                    invoice_id=invoice.id,
                    product_id=product.id,
                    quantity=qty,
                    amount=amount
                )
                db.session.add(item)
        
        # Check inventory availability
        is_available, error_msg = InvoiceService.validate_inventory_availability(new_items)
        if not is_available:
            flash(error_msg, 'error')
            db.session.rollback()
            return render_template('invoices/edit.html', invoice=invoice, customers=customers, products=products_data)
        
        invoice.total_amount = total_amount
        db.session.commit()
        
        # Restore old inventory and decrease new inventory
        for product_id, old_qty in old_quantities.items():
            product = Product.query.get(product_id)
            if product:
                product.quantity += old_qty
        
        InvoiceService.decrease_inventory(new_items)
        
        flash('Invoice updated successfully!', 'success')
        return redirect(url_for('frontend.invoice_list'))
    
    return render_template('invoices/edit.html', invoice=invoice, customers=customers, products=products_data)

@frontend_bp.route('/invoices/list')
@jwt_required()
@permission_required('Invoice', 'read')
def invoice_list_alt():
    invoices = InvoiceService.get_accessible_invoices()
    return render_template('invoices/list.html', invoices=invoices)

@frontend_bp.route('/invoices/create', methods=['GET'])
def create_invoice():
    return render_template(
        'invoices/create.html',
        date=datetime.utcnow().strftime('%Y-%m-%d')
    )

@frontend_bp.route('/invoices/delete/<int:invoice_id>')
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)

    # delete details first
    InvoiceProduct.query.filter_by(invoice_id=invoice.id).delete()

    # delete master
    db.session.delete(invoice)
    db.session.commit()

    return redirect(url_for('frontend.invoice_list'))
