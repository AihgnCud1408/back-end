from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, Role

class UserService:
    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def change_role(db:Session, user_id: int, role: Role):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found.")

        user.role = role
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")

        db.delete(user)
        db.commit()
        return None
