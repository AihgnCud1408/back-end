from sqlalchemy import Column, Integer, String, Enum
import enum
from app.db.session import Base

class Role(str, enum.Enum):
    student = "student"
    lecturer = "lecturer"
    admin = "admin"
    it = "it"
    technician = "technician"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(Enum(Role), nullable=False)
    password_hash = Column(String(255), nullable=False)
