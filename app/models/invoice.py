from app import db
from app.models.base import BaseModel
from datetime import datetime

class Invoice(BaseModel):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey('customers.id'),
        nullable=False
    )

    invoice_date = db.Column(db.DateTime, default=datetime.utcnow)

    total_amount = db.Column(db.Float, default=0)

    status = db.Column(
        db.String(20),
        default='pending'
    )

    customer = db.relationship('Customer', backref='invoices')
