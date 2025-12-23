from app import create_app, db
from datetime import datetime, timedelta
from app.models.customer import Customer
from app.models.product import Product
from app.models.invoice import Invoice
from app.models.invoice_product import InvoiceProduct
from app.models.user import User

def create_sample_data():
    """Create sample test data for Invoice Management System"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        InvoiceProduct.query.delete()
        Invoice.query.delete()
        Product.query.delete()
        Customer.query.delete()
        User.query.delete()
        db.session.commit()
        
        # Create 3 customers
        customers = [
            Customer(
                name="John Smith",
                email="john.smith@example.com",
                address="123 Main Street, New York, NY 10001",
                phone="212-555-1234",
                mobile="917-555-5678"
            ),
            Customer(
                name="Sarah Johnson",
                email="sarah.johnson@example.com",
                address="456 Oak Avenue, Los Angeles, CA 90001",
                phone="213-555-9876",
                mobile="310-555-5432"
            ),
            Customer(
                name="Michael Davis",
                email="michael.davis@example.com",
                address="789 Pine Road, Chicago, IL 60601",
                phone="312-555-2468",
                mobile="773-555-1357"
            )
        ]
        
        for customer in customers:
            db.session.add(customer)
        db.session.commit()
        
        # Create 5 products
        products = [
            Product(
                name="Laptop Computer",
                price=1299.99,
                quantity=50,
                description="High-performance laptop with 16GB RAM and 512GB SSD"
            ),
            Product(
                name="Wireless Mouse",
                price=29.99,
                quantity=100,
                description="Ergonomic wireless mouse with precision tracking"
            ),
            Product(
                name="Mechanical Keyboard",
                price=89.99,
                quantity=75,
                description="RGB mechanical keyboard with blue switches"
            ),
            Product(
                name="24-inch Monitor",
                price=249.99,
                quantity=30,
                description="Full HD LED monitor with HDMI and DisplayPort"
            ),
            Product(
                name="USB-C Hub",
                price=49.99,
                quantity=60,
                description="7-in-1 USB-C hub with 4K HDMI support"
            )
        ]
        
        for product in products:
            db.session.add(product)
        db.session.commit()
        
        # Create test user
        test_user = User(
            email="admin@test.com",
            role_id=1
        )
        test_user.set_password("admin123")
        db.session.add(test_user)
        db.session.commit()
        
        # Create 5 invoices with realistic data
        base_date = datetime.now() - timedelta(days=30)
        
        # Invoice 1: PAID - Customer 1 - Multiple items
        invoice1 = Invoice(
            customer_id=1,
            invoice_date=base_date + timedelta(days=5),
            status="paid",
            created_at=base_date + timedelta(days=5),
            created_by=1,
            updated_at=base_date + timedelta(days=5),
            updated_by=1
        )
        db.session.add(invoice1)
        db.session.flush()  # Get the ID
        
        # Invoice 1 products
        invoice1_products = [
            InvoiceProduct(
                invoice_id=invoice1.id,
                product_id=1,  # Laptop
                quantity=1,
                amount=1299.99
            ),
            InvoiceProduct(
                invoice_id=invoice1.id,
                product_id=2,  # Mouse
                quantity=1,
                amount=29.99
            ),
            InvoiceProduct(
                invoice_id=invoice1.id,
                product_id=3,  # Keyboard
                quantity=1,
                amount=89.99
            )
        ]
        
        total1 = 1299.99 + 29.99 + 89.99
        invoice1.total_amount = total1
        
        for ip in invoice1_products:
            db.session.add(ip)
        
        # Invoice 2: PENDING - Customer 2 - Single item
        invoice2 = Invoice(
            customer_id=2,
            invoice_date=base_date + timedelta(days=10),
            status="pending",
            created_at=base_date + timedelta(days=10),
            created_by=1,
            updated_at=base_date + timedelta(days=10),
            updated_by=1
        )
        db.session.add(invoice2)
        db.session.flush()
        
        invoice2_products = [
            InvoiceProduct(
                invoice_id=invoice2.id,
                product_id=4,  # Monitor
                quantity=2,
                amount=249.99 * 2
            )
        ]
        
        total2 = 499.98
        invoice2.total_amount = total2
        
        for ip in invoice2_products:
            db.session.add(ip)
        
        # Invoice 3: PAID - Customer 3 - Multiple quantities
        invoice3 = Invoice(
            customer_id=3,
            invoice_date=base_date + timedelta(days=15),
            status="paid",
            created_at=base_date + timedelta(days=15),
            created_by=1,
            updated_at=base_date + timedelta(days=15),
            updated_by=1
        )
        db.session.add(invoice3)
        db.session.flush()
        
        invoice3_products = [
            InvoiceProduct(
                invoice_id=invoice3.id,
                product_id=5,  # USB-C Hub
                quantity=5,
                amount=49.99 * 5
            ),
            InvoiceProduct(
                invoice_id=invoice3.id,
                product_id=2,  # Mouse
                quantity=3,
                amount=29.99 * 3
            )
        ]
        
        total3 = (49.99 * 5) + (29.99 * 3)
        invoice3.total_amount = total3
        
        for ip in invoice3_products:
            db.session.add(ip)
        
        # Invoice 4: CANCELLED - Customer 1 - Single item
        invoice4 = Invoice(
            customer_id=1,
            invoice_date=base_date + timedelta(days=20),
            status="cancelled",
            created_at=base_date + timedelta(days=20),
            created_by=1,
            updated_at=base_date + timedelta(days=22),
            updated_by=1
        )
        db.session.add(invoice4)
        db.session.flush()
        
        invoice4_products = [
            InvoiceProduct(
                invoice_id=invoice4.id,
                product_id=3,  # Keyboard
                quantity=1,
                amount=89.99
            )
        ]
        
        total4 = 89.99
        invoice4.total_amount = total4
        
        for ip in invoice4_products:
            db.session.add(ip)
        
        # Invoice 5: PENDING - Customer 2 - Large order
        invoice5 = Invoice(
            customer_id=2,
            invoice_date=base_date + timedelta(days=25),
            status="pending",
            created_at=base_date + timedelta(days=25),
            created_by=1,
            updated_at=base_date + timedelta(days=25),
            updated_by=1
        )
        db.session.add(invoice5)
        db.session.flush()
        
        invoice5_products = [
            InvoiceProduct(
                invoice_id=invoice5.id,
                product_id=1,  # Laptop
                quantity=2,
                amount=1299.99 * 2
            ),
            InvoiceProduct(
                invoice_id=invoice5.id,
                product_id=4,  # Monitor
                quantity=3,
                amount=249.99 * 3
            ),
            InvoiceProduct(
                invoice_id=invoice5.id,
                product_id=5,  # USB-C Hub
                quantity=10,
                amount=49.99 * 10
            )
        ]
        
        total5 = (1299.99 * 2) + (249.99 * 3) + (49.99 * 10)
        invoice5.total_amount = total5
        
        for ip in invoice5_products:
            db.session.add(ip)
        
        # Commit all data
        db.session.commit()
        
        # Print summary
        print("Sample data created successfully!")
        print(f"Customers: {Customer.query.count()}")
        print(f"Products: {Product.query.count()}")
        print(f"Invoices: {Invoice.query.count()}")
        print(f"Invoice Products: {InvoiceProduct.query.count()}")
        
        print("\nInvoice Summary:")
        invoices = Invoice.query.all()
        for inv in invoices:
            print(f"Invoice #{inv.id}: Customer {inv.customer_id}, Status: {inv.status}, Total: ${inv.total_amount:.2f}")
        
        print(f"\nTotal Amounts by Status:")
        paid_total = sum(inv.total_amount for inv in Invoice.query.filter_by(status='paid').all())
        pending_total = sum(inv.total_amount for inv in Invoice.query.filter_by(status='pending').all())
        cancelled_total = sum(inv.total_amount for inv in Invoice.query.filter_by(status='cancelled').all())
        
        print(f"Paid: ${paid_total:.2f}")
        print(f"Pending: ${pending_total:.2f}")
        print(f"Cancelled: ${cancelled_total:.2f}")
        print(f"Grand Total: ${paid_total + pending_total + cancelled_total:.2f}")

if __name__ == "__main__":
    create_sample_data()
