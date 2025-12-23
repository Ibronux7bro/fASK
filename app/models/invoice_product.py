from app import db
from app.models.base import BaseModel

class InvoiceProduct(BaseModel):
    __tablename__ = 'invoice_products'

    id = db.Column(db.Integer, primary_key=True)

    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey('invoices.id'),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)

    amount = db.Column(db.Float, nullable=False)

    invoice = db.relationship('Invoice', backref='items')
    product = db.relationship('Product')
