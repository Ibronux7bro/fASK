from typing import List, Optional, Dict, Any
from app.models.role import Role
from app.models.permission import Permission
from app import db


class RoleService:
    """Service layer for role hierarchy and RBAC business logic"""
    
    # Define role hierarchy: Admin → Sales Manager → Sales Employee → Cashier
    ROLE_HIERARCHY = {
        'Admin': None,  # Top level
        'Sales Manager': 'Admin',
        'Sales Employee': 'Sales Manager', 
        'Cashier': 'Sales Employee'
    }
    
    @staticmethod
    def create_role_hierarchy() -> Dict[str, int]:
        """Create the role hierarchy and return role name to ID mapping"""
        role_map = {}
        
        # Create roles in hierarchy order (top to bottom)
        for role_name, parent_name in RoleService.ROLE_HIERARCHY.items():
            # Check if role already exists
            existing_role = Role.query.filter_by(name=role_name).first()
            if existing_role:
                role_map[role_name] = existing_role.id
                continue
                
            # Create new role with correct parent_role_id
            parent_role_id = None
            if parent_name and parent_name in role_map:
                parent_role_id = role_map[parent_name]
            
            role = Role(
                name=role_name,
                parent_role_id=parent_role_id,
                status=True
            )
            db.session.add(role)
            db.session.flush()  # Get the ID
            role_map[role_name] = role.id
        
        db.session.commit()
        return role_map
    
    @staticmethod
    def get_child_role_ids(parent_role_id: int) -> List[int]:
        """Get all child role IDs recursively"""
        child_ids = []
        children = Role.query.filter_by(parent_role_id=parent_role_id).all()
        
        for child in children:
            child_ids.append(child.id)
            # Recursively get children of this child
            child_ids.extend(RoleService.get_child_role_ids(child.id))
        
        return child_ids
    
    @staticmethod
    def can_manage_role(manager_role_id: int, target_role_id: int) -> bool:
        """Check if manager role can manage target role"""
        # Admin can manage everyone
        manager_role = Role.query.get(manager_role_id)
        if manager_role and manager_role.name == 'Admin':
            return True
        
        # Check if target_role is a child of manager_role
        child_ids = RoleService.get_child_role_ids(manager_role_id)
        return target_role_id in child_ids
    
    @staticmethod
    def is_same_level(role_id_1: int, role_id_2: int) -> bool:
        """Check if two roles are at the same hierarchy level"""
        role1 = Role.query.get(role_id_1)
        role2 = Role.query.get(role_id_2)
        
        if not role1 or not role2:
            return False
        
        # Same parent means same level
        return role1.parent_role_id == role2.parent_role_id
    
    @staticmethod
    def get_role_level(role_id: int) -> int:
        """Get the hierarchy level of a role (Admin=0, Sales Manager=1, etc.)"""
        role = Role.query.get(role_id)
        if not role:
            return -1
        
        level = 0
        current_role = role
        
        while current_role.parent_role_id:
            level += 1
            current_role = Role.query.get(current_role.parent_role_id)
            if not current_role:
                break
        
        return level
    
    @staticmethod
    def assign_parent_role_from_backend(role_name: str) -> Optional[int]:
        """Assign parent_role_id based on role name (backend logic only)"""
        parent_name = RoleService.ROLE_HIERARCHY.get(role_name)
        if not parent_name:
            return None
        
        parent_role = Role.query.filter_by(name=parent_name).first()
        return parent_role.id if parent_role else None
