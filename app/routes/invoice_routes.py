from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.invoice import Invoice
from app.models.invoice_product import InvoiceProduct
from app.models.product import Product
from app.models.customer import Customer
from app.validations.invoice_validation import InvoiceValidation

invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/seed', methods=['POST'])
def create_seed():
    try:
        # Create customers
        if Customer.query.count() == 0:
            customers = [
                Customer(name="John Doe", email="john@test.com"),
                Customer(name="Jane Smith", email="jane@test.com"), 
                Customer(name="Bob Johnson", email="bob@test.com")
            ]
            for c in customers:
                db.session.add(c)
        
        # Create products
        if Product.query.count() == 0:
            products = [
                Product(name="Laptop", price=999.99, quantity=50),
                Product(name="Mouse", price=29.99, quantity=100),
                Product(name="Keyboard", price=49.99, quantity=75)
            ]
            for p in products:
                db.session.add(p)
        
        db.session.commit()
        return jsonify({"message": "Test data created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE INVOICE
@invoice_bp.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    data = request.get_json()

    #  Validation BEFORE CRUD
    errors = InvoiceValidation.create_invoice_validation(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Check if customer exists
    from app.models.customer import Customer
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({"error": f"Customer with ID {data['customer_id']} not found"}), 400

    # Create invoice (MASTER)
    invoice = Invoice(
        customer_id=data['customer_id'],
        status='pending'
    )
    db.session.add(invoice)
    db.session.commit()

    total_amount = 0

    # Create invoice items (DETAIL)
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({"error": f"Product with ID {item['product_id']} not found"}), 400
        
        amount = product.price * item['quantity']
        total_amount += amount

        invoice_item = InvoiceProduct(
            invoice_id=invoice.id,
            product_id=product.id,
            quantity=item['quantity'],
            amount=amount
        )
        db.session.add(invoice_item)

    invoice.total_amount = total_amount
    db.session.commit()

    return jsonify({
        "message": "Invoice created successfully",
        "invoice_id": invoice.id
    }), 201


#  READ INVOICES
@invoice_bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    invoices = Invoice.query.all()

    result = []
    for inv in invoices:
        result.append({
            "id": inv.id,
            "customer_id": inv.customer_id,
            "total_amount": inv.total_amount,
            "status": inv.status
        })

    return jsonify(result), 200


#  UPDATE INVOICE
@invoice_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
@jwt_required()
def update_invoice(invoice_id):
    data = request.get_json()

    # Validation BEFORE CRUD
    errors = InvoiceValidation.update_invoice_validation(data)
    if errors:
        return jsonify({"errors": errors}), 400

    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.status = data['status']
    db.session.commit()

    return jsonify({"message": "Invoice updated successfully"}), 200


#  DELETE INVOICE
@invoice_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)

    # delete details first (DETAIL)
    InvoiceProduct.query.filter_by(invoice_id=invoice.id).delete()

    # delete master
    db.session.delete(invoice)
    db.session.commit()

    return jsonify({"message": "Invoice deleted successfully"}), 200
