import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def validate_production_settings():
    """Validate that production environment has secure settings."""
    
    if settings.ENVIRONMENT == "production":
        # Check encryption key
        if not settings.ENCRYPTION_KEY or len(settings.ENCRYPTION_KEY) < 32:
            raise ValueError(
                "PRODUCTION MODE: ENCRYPTION_KEY not set or too short!\n"
                "Generate with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
            )
        
        # Check JWT secret
        if (settings.JWT_SECRET == "CHANGE_THIS_IN_PRODUCTION_USE_RANDOM_64_CHAR_STRING" or
            len(settings.JWT_SECRET) < 32):
            raise ValueError(
                "PRODUCTION MODE: JWT_SECRET is weak or default!\n"
                "Set a strong 64+ character random string in .env"
            )
        
        # Check debug flag
        if settings.DEBUG:
            raise ValueError("PRODUCTION MODE: DEBUG must be False!")
        
        logger.info("✅ Production security validation passed")
