from app import db
from app.models.base import BaseModel

class Role(BaseModel):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)

    parent_role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id'),
        nullable=True
    )

    parent = db.relationship(
        'Role',
        remote_side=[id],
        backref='children'
    )
