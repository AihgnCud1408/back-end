from pydantic import BaseModel, EmailStr
from enum import Enum

class Role(str, Enum):
    student = "student"
    lecturer = "lecturer"
    admin = "admin"
    it = "it"
    technician = "technician"

class UserCreateSchema(BaseModel):
    user_code: int
    name: str
    email: EmailStr
    role: Role
    password: str

class UserReadSchema(BaseModel):
    user_code: int
    name: str
    email: EmailStr
    role: Role

    class Config:
        orm_mode = True
