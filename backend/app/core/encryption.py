"""
Fernet symmetric encryption helpers for at-rest credential storage.

Uses ENCRYPTION_KEY from settings.  When the key is not configured the
helpers become a no-op passthrough so local development without a key
is not blocked.
"""

from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings


def encrypt(value: str) -> str:
    """Encrypt a string using Fernet symmetric encryption."""
    if not value or not settings.ENCRYPTION_KEY:
        return value  # fallback: store as-is if no key configured
    try:
        f = Fernet(settings.ENCRYPTION_KEY.encode())
        return f.encrypt(value.encode()).decode()
    except Exception:
        return value


def decrypt(value: str) -> str:
    """Decrypt a Fernet-encrypted string."""
    if not value or not settings.ENCRYPTION_KEY:
        return value  # fallback
    try:
        f = Fernet(settings.ENCRYPTION_KEY.encode())
        return f.decrypt(value.encode()).decode()
    except (InvalidToken, Exception):
        return value  # if decryption fails, return as-is
