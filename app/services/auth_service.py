from fastapi import HTTPException

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:

    @staticmethod
    def register(db, payload):

        if UserRepository.get_by_email(db, payload.email):
            raise HTTPException(400, "Email already registered")
        
        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            role=payload.role
        )

        return UserRepository.create(db, user)


    @staticmethod
    def login(db, payload):

        user = UserRepository.get_by_email(db, payload.email)

        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")
        
        token = create_access_token(
            {"sub": str(user.id)}
        )

        return {"access_token": token, "token_type": "bearer"}