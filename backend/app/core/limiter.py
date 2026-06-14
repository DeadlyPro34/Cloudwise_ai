"""
Rate limiting configuration using slowapi.
Per Security Policy: protects auth and copilot endpoints from abuse.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

if settings.REDIS_URL:
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=settings.REDIS_URL,
        default_limits=["200/minute"],
    )
else:
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri="memory://",
        default_limits=["200/minute"],
    )
