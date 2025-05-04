from fastapi import Depends, HTTPException, status
from typing import List
from app.models.user import Role, User
from app.services.auth_service import get_current_user

def require_roles(allowed_roles: List[Role]):
    def _checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Permission Denied")
        return user
    return Depends(_checker)
