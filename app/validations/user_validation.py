import re
from app.models.user import User

class UserValidation:

    @staticmethod
    def validate_create(data):
        errors = []

        # required fields
        if not data.get('name'):
            errors.append('Name is required')

        if not data.get('email'):
            errors.append('Email is required')

        if not data.get('password'):
            errors.append('Password is required')

        # email format
        if data.get('email'):
            email_regex = r'^[^@]+@[^@]+\.[^@]+$'
            if not re.match(email_regex, data['email']):
                errors.append('Invalid email format')

        # password length
        if data.get('password') and len(data['password']) < 6:
            errors.append('Password must be at least 6 characters')

        # unique email
        if data.get('email'):
            if User.query.filter_by(email=data['email']).first():
                errors.append('Email already exists')

        return errors
