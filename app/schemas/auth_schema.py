from pydantic import BaseModel
from app.schemas.user_schema import Role

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    role: Role

    class Config:
        orm_mode = True