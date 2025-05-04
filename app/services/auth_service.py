from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.models.user import User, Role
from app.schemas.auth_schema import TokenSchema
from app.utils.security import hash_password, verify_password, create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from pydantic import EmailStr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
        return user
    except:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")

class AuthService:
    @staticmethod
    def register(db: Session, name: str, email: EmailStr, role: Role, password: str):
        if role in [Role.admin, Role.technician, Role.it]:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Permission denied.")

        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered.")

        hashed_password = hash_password(password)
        user = User(
            name=name,
            email=str(email),
            role=role,
            password_hash=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            return None
        token = create_access_token({"sub": user.email})
        return TokenSchema(
            access_token=token,
            token_type="bearer",
            role=user.role
        )
