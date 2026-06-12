"""
Rate limiting configuration using slowapi.
Per Security Policy: protects auth and copilot endpoints from abuse.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
