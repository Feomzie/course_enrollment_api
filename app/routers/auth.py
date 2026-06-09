from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, auth_rate_limit
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserResponse, dependencies=[Depends(auth_rate_limit)])
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register(db, payload)

@router.post("/login", response_model=TokenResponse, dependencies=[Depends(auth_rate_limit)])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login(db, payload)


@router.get("/me", response_model=UserResponse)
def me(user=Depends(get_current_user)):
    return user