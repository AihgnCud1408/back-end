from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreateSchema, UserReadSchema
from app.schemas.auth_schema import TokenSchema
from app.db.session import get_db
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/signup", response_model=UserReadSchema)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    return AuthService.register(
        db,
        user.name,
        user.email,
        user.role,
        user.password
    )

@router.post("/login", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = AuthService.login(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password")
    return token
