"""
Authentication API routes.

Per Implementation Plan Milestone 1:
  POST /auth/register
  POST /auth/login

Per Security Policy: rate limited (5/minute) to prevent brute-force/credential stuffing.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    MessageResponse,
)
from app.services.auth_service import register_user, authenticate_user, AuthError
import secrets
from datetime import timedelta
from sqlalchemy import select
from app.core.security import hash_password
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_REGISTER)
def register(request: Request, payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account and return an access token."""
    try:
        user = register_user(
            db,
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
        logger.info("Registration successful", extra={
            "email": payload.email,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip": request.client.host if request.client else None,
        })
    except AuthError as e:
        logger.warning("Registration failed", extra={
            "email": payload.email,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip": request.client.host if request.client else None,
            "reason": str(e)
        })
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    access_token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=access_token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.RATE_LIMIT_LOGIN)
def login(request: Request, payload: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate and return an access token."""
    try:
        user = authenticate_user(db, email=payload.email, password=payload.password)
        logger.info("Login successful", extra={
            "email": payload.email,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip": request.client.host if request.client else None,
        })
    except AuthError as e:
        logger.warning("Login failed", extra={
            "email": payload.email,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip": request.client.host if request.client else None,
            "reason": str(e)
        })
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    access_token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=access_token, user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return UserResponse.model_validate(current_user)

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    
    token = secrets.token_urlsafe(32)
    message = "Password reset initiated"
    note = "In production this token would be emailed. Use this token to reset your password."
    
    if user:
        user.reset_token = token
        user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
        db.commit()
        
    return {"message": message, "reset_token": token, "note": note}

@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.reset_token == payload.token)).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
    if user.reset_token_expires:
        expires = user.reset_token_expires
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if expires < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Reset token has expired. Please request a new one.")
        
    user.password_hash = hash_password(payload.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return {"message": "Password reset successfully. You can now log in."}
