import bcrypt
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import settings

# Use bcrypt_sha256 so passwords longer than 72 bytes are handled safely.
# Existing bcrypt hashes remain supported for verification.
pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")


def hash_password(password:str)-> str:
    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password.decode("utf-8")
	

def verify_password(plain_password: str, hashed_password: str)-> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf=8")
    )


def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )