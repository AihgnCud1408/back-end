import bcrypt
from datetime import datetime, timedelta
import jwt
from app.config import config

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=config.jwt_expire)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.jwt_secret, algorithm=config.jwt_algorithm)

def decode_access_token(token: str):
    return jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])
