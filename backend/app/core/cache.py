"""Redis-backed caching with granular invalidation."""

import json
import logging
from redis import Redis
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)

class CacheManager:
    """Manage application caching with Redis."""
    
    def __init__(self, redis_client: Redis | None = None):
        self.redis = redis_client
        self.enabled = redis_client is not None
    
    def get(self, key: str) -> Any | None:
        """Get cached value by key."""
        if not self.enabled:
            return None
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache GET error: {e}", extra={"key": key})
            return None
    
    def set(self, key: str, value: Any, expire_seconds: int = 300) -> None:
        """Set cached value with TTL."""
        if not self.enabled:
            return
        try:
            self.redis.setex(key, expire_seconds, json.dumps(value))
            logger.debug(f"Cache SET", extra={"key": key, "ttl": expire_seconds})
        except Exception as e:
            logger.warning(f"Cache SET error: {e}", extra={"key": key})
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern (e.g., 'org:123:*')."""
        if not self.enabled:
            return 0
        try:
            keys = self.redis.keys(pattern)
            if keys:
                count = self.redis.delete(*keys)
                logger.info(f"Cache invalidated", extra={
                    "pattern": pattern,
                    "count": count,
                })
                return count
            return 0
        except Exception as e:
            logger.warning(f"Cache INVALIDATE error: {e}", extra={"pattern": pattern})
            return 0
    
    def invalidate_org(self, org_id: str) -> int:
        """Clear all cache for specific organization."""
        return self.invalidate_pattern(f"org:{org_id}:*")
    
    def invalidate_account(self, account_id: str) -> int:
        """Clear all cache for specific AWS account."""
        return self.invalidate_pattern(f"account:{account_id}:*")
    
    def invalidate_user(self, user_id: str) -> int:
        """Clear all cache for specific user."""
        return self.invalidate_pattern(f"user:{user_id}:*")

# Global cache manager instance
cache_manager: CacheManager | None = None

def cache(expire_seconds: int = 300, key_prefix: str = ""):
    """
    Decorator for caching function results.
    
    Usage:
        @cache(expire_seconds=300)
        async def get_data(user_id: str):
            return {...}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            args_str = "_".join(str(a) for a in args)
            kwargs_str = "_".join(f"{k}_{v}" for k, v in sorted(kwargs.items()))
            func_key = f"{key_prefix or func.__name__}"
            cache_key = f"{func_key}:{args_str}:{kwargs_str}".replace(" ", "_")
            
            # Try to get from cache
            cached = cache_manager.get(cache_key) if cache_manager else None
            if cached is not None:
                logger.debug(f"Cache hit", extra={"key": cache_key})
                return cached
            
            # Compute result
            result = await func(*args, **kwargs)
            
            # Store in cache
            if cache_manager:
                cache_manager.set(cache_key, result, expire_seconds)
            
            return result
        
        return wrapper
    return decorator
