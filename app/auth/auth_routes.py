from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.validators.user_validator import UserValidator
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login - returns JWT token"""
    try:
        data = request.get_json() or {}
        
        # Validate input data
        validated_data = UserValidator.validate_login({
            'email': data.get('email'),
            'password': data.get('password')
        })
        
        user = User.query.filter_by(email=validated_data['email']).first()
        
        if not user or not user.check_password(validated_data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        if not user.status:
            return jsonify({'message': 'Account is inactive'}), 401
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'role_id': user.role_id,
                'role_name': user.role.name if user.role else None
            }
        )
        
        response = jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role.name if user.role else None
            }
        })
        
        # Set the JWT token in an HTTP-only cookie
        response.set_cookie(
            key='access_token',
            value=f'Bearer {access_token}',
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            max_age=86400  # 1 day
        )
        
        return response, 200
        
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 400


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role.name if user.role else None,
            'status': user.status
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get user info', 'error': str(e)}), 400
