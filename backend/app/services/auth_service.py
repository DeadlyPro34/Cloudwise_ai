"""
Authentication service - business logic for registration and login.
Also creates a default Organization for each new user (per schema design).
"""

import re
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.models.organization import Organization
from app.core.security import hash_password, verify_password


class AuthError(Exception):
    """Raised for authentication-related errors (bad credentials, duplicate email, etc.)."""
    pass


def _slugify(text: str) -> str:
    """Create a URL-safe slug from text, with a random suffix for uniqueness."""
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    suffix = uuid.uuid4().hex[:8]
    return f"{base}-{suffix}" if base else f"org-{suffix}"


def register_user(db: Session, email: str, password: str,
                   first_name: str | None = None, last_name: str | None = None) -> User:
    """
    Register a new user and create their default organization.

    Raises:
        AuthError: if the email is already registered.
    """
    existing = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if existing:
        raise AuthError("An account with this email already exists.")

    user = User(
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
    )
    db.add(user)
    db.flush()  # get user.id without committing yet

    # Create a default organization for this user (per schema design)
    org_name = first_name or email.split("@")[0]
    org = Organization(
        name=f"{org_name}'s Organization",
        slug=_slugify(org_name),
        owner_id=user.id,
    )
    db.add(org)

    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Verify credentials and return the user.

    Raises:
        AuthError: if credentials are invalid or account is inactive.
    """
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        raise AuthError("Invalid email or password.")

    if not user.is_active:
        raise AuthError("This account has been deactivated.")

    user.last_login = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()


def get_user_organization(db: Session, user_id: uuid.UUID) -> Organization | None:
    return db.execute(
        select(Organization).where(Organization.owner_id == user_id)
    ).scalar_one_or_none()
