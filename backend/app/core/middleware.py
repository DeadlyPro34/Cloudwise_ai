"""
Security headers middleware.
Per Security Policy: mitigates clickjacking, MIME attacks, XSS, transport downgrade.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if settings.ENVIRONMENT != "development":
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        # CSP kept permissive for API responses (mainly JSON); tighten if serving HTML.
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response

import logging
import time
import json
from fastapi import Request

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses to JSON logger."""
    
    SKIP_PATHS = {"/health", "/docs", "/openapi.json"}
    
    async def dispatch(self, request: Request, call_next):
        """Log request/response with metrics."""
        
        # Skip logging for health checks and API docs
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)
        
        # Log request
        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        logger.info("request_started", extra={
            "method": request.method,
            "path": request.url.path,
            "client_ip": client_host,
            "user_agent": user_agent,
        })
        
        try:
            # Process request
            response = await call_next(request)
            
            # Log response with metrics
            duration_ms = (time.time() - start_time) * 1000
            
            logger.info("request_completed", extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "client_ip": client_host,
            })
            
            return response
            
        except Exception as exc:
            # Log error
            duration_ms = (time.time() - start_time) * 1000
            
            logger.error("request_failed", extra={
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration_ms, 2),
                "error": str(exc),
                "client_ip": client_host,
            })
            
            raise
