from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.user_schema import UserReadSchema, Role
from app.services.user_service import UserService
from app.utils.rbac import require_roles

router = APIRouter(prefix="/it", tags=["it"], dependencies=[require_roles([Role.it])])

@router.get("/users", response_model=List[UserReadSchema])
def get_all_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)

@router.patch("/users/{user_id}", response_model=UserReadSchema)
def change_role(user_id: int, role: Role, db: Session = Depends(get_db)):
    return UserService.change_role(db, user_id, role)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.delete_user(db, user_id)
