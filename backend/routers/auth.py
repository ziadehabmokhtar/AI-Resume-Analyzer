from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models import User
from backend.schemas import UserRegister, Token
from backend.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=Token, status_code=201, summary="Register a new user"
)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email is already registered")
    user = User(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return Token(access_token=create_access_token(user.id))


@router.post("/login", response_model=Token, summary="Login")
def login(data: UserRegister, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return Token(access_token=create_access_token(user.id))


@router.post("/logout", summary="Logout")
def logout(user=Depends(get_current_user)):
    return {"message": "Logout acknowledged. Remove the bearer token on the client."}


@router.get("/me", summary="Get current user")
def me(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email}
