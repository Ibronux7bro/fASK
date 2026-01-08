from app import db
from app.models.base import BaseModel

class Permission(BaseModel):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)

    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id'),
        nullable=False
    )

    model_name = db.Column(db.String(100), nullable=False)

    can_create = db.Column(db.Boolean, default=False)
    can_read   = db.Column(db.Boolean, default=False)
    can_update = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)

    role = db.relationship('Role', backref='permissions')
