"""Structured JSON logging for production audit trails."""

import logging
import json
import os
from pythonjsonlogger import jsonlogger

def setup_logging(log_level: str = "INFO"):
    """Configure JSON logging to stdout and file."""
    
    # Get or create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # JSON formatter
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(timestamp)s %(level)s %(name)s %(message)s',
        timestamp=True,
    )
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if logs directory exists)
    if os.path.exists('logs'):
        file_handler = logging.FileHandler('logs/cloudwise.log')
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
    
    # Set other library loggers to WARNING (reduce noise)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    return logger
