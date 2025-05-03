from pydantic import BaseModel, EmailStr
from app.schemas.user_schema import Role

class UserInfoSchema(BaseModel):
    id: int
    email: EmailStr
    role: Role

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    user: UserInfoSchema

    class Config:
        orm_mode = True