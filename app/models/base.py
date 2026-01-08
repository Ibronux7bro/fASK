from datetime import datetime
from app import db
from sqlalchemy.orm import declared_attr

class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    @declared_attr
    def creator(cls):
        # Exclude User model to avoid circular relationships
        if cls.__name__ == 'User':
            return None
        return db.relationship('User', foreign_keys=lambda: cls.created_by, backref=f'{cls.__tablename__}_created')

    @declared_attr
    def updater(cls):
        # Exclude User model to avoid circular relationships
        if cls.__name__ == 'User':
            return None
        return db.relationship('User', foreign_keys=lambda: cls.updated_by, backref=f'{cls.__tablename__}_updated')
