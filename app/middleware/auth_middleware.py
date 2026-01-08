from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


def token_required(f):
    """Decorator to verify JWT token in request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # First try to verify the token from the Authorization header
            try:
                verify_jwt_in_request()
                return f(*args, **kwargs)
            except:
                # If that fails, try to get the token from cookies
                token = request.cookies.get('access_token')
                if token:
                    # Set the Authorization header with the token from cookies
                    request.headers['Authorization'] = f'Bearer {token}'
                    verify_jwt_in_request()
                    return f(*args, **kwargs)
                else:
                    # If no token is found in cookies, return 401
                    return jsonify({'message': 'Invalid or missing token'}), 401
        except Exception as e:
            return jsonify({'message': 'Invalid or missing token', 'error': str(e)}), 401
    return decorated_function


def permission_required(model_name: str, action: str):
    """
    Decorator to check user permissions for specific model and action
    action: 'create', 'read', 'update', 'delete'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                
                # Get current user
                current_user_id = get_jwt_identity()
                print(f"DEBUG: User ID from Token: {current_user_id}") # DEBUG
                user = User.query.get(current_user_id)
                
                if not user:
                    print(f"DEBUG: User not found for ID {current_user_id}") # DEBUG
                    return jsonify({'message': 'User not found'}), 401
                
                # Get user role
                print(f"DEBUG: User Role ID: {user.role_id}") # DEBUG
                role = Role.query.get(user.role_id)
                if not role:
                    print(f"DEBUG: Role not found for ID {user.role_id}") # DEBUG
                    return jsonify({'message': 'Role not found'}), 401
                
                # Check permission
                print(f"DEBUG: Checking permission for Role {role.name} on {model_name}") # DEBUG
                permission = Permission.query.filter_by(
                    role_id=role.id,
                    model_name=model_name
                ).first()
                
                if not permission:
                    print(f"DEBUG: Permission entry not found for Role {role.id} Model {model_name}") # DEBUG
                    return jsonify({'message': 'Permission not found'}), 403
                
                # Check specific action permission
                action_map = {
                    'create': permission.can_create,
                    'read': permission.can_read,
                    'update': permission.can_update,
                    'delete': permission.can_delete
                }
                
                if not action_map.get(action, False):
                    print(f"DEBUG: Insufficient permissions: {action} is False") # DEBUG
                    return jsonify({'message': f'Insufficient permissions for {action} on {model_name}'}), 403
                
                # Add user and role to request context
                request.current_user = user
                request.current_role = role
                
                return f(*args, **kwargs)
                
            except Exception as e:
                import traceback
                traceback.print_exc() # DEBUG
                print(f"DEBUG: Authorization Error: {str(e)}") # DEBUG
                return jsonify({'message': 'Authorization error', 'details': str(e)}), 401
                
        return decorated_function
    return decorator


def role_required(required_role_name: str):
    """Decorator to check if user has specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                
                # Get current user
                current_user_id = get_jwt_identity()
                user = User.query.get(current_user_id)
                
                if not user:
                    return jsonify({'message': 'User not found'}), 401
                
                # Get user role
                role = Role.query.get(user.role_id)
                if not role or role.name != required_role_name:
                    return jsonify({'message': f'{required_role_name} role required'}), 403
                
                # Add user and role to request context
                request.current_user = user
                request.current_role = role
                
                return f(*args, **kwargs)
                
            except Exception as e:
                return jsonify({'message': 'Authorization error'}), 401
                
        return decorated_function
    return decorator


def can_manage_role(target_role_id: int):
    """Check if current user can manage target role (hierarchy check)"""
    try:
        verify_jwt_in_request()
        
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return False
        
        # Get user role
        user_role = Role.query.get(user.role_id)
        if not user_role:
            return False
        
        # Admin can manage everyone
        if user_role.name == 'Admin':
            return True
        
        # Get target role
        target_role = Role.query.get(target_role_id)
        if not target_role:
            return False
        
        # Check if target role is in user's hierarchy (child roles)
        return is_child_role(target_role, user_role)
        
    except Exception:
        return False


def is_child_role(role: Role, parent_role: Role) -> bool:
    """Recursively check if role is a child of parent_role"""
    if role.parent_role_id == parent_role.id:
        return True
    
    if role.parent_role_id:
        parent = Role.query.get(role.parent_role_id)
        if parent:
            return is_child_role(parent, parent_role)
    
    return False
