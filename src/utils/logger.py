"""
Logging configuration for FastAPI application.

Provides structured logging with both console and file handlers.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str = "fastapi_app",
    log_level: int = logging.INFO,
    log_dir: str = "logs"
) -> logging.Logger:
    """
    Configure and return a logger with console and file handlers.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler (INFO level and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File Handler - All levels
    log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=10_485_760,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error File Handler - ERROR and CRITICAL only
    error_log_file = os.path.join(log_dir, f"error_{datetime.now().strftime('%Y%m%d')}.log")
    error_handler = logging.handlers.RotatingFileHandler(
        filename=error_log_file,
        maxBytes=10_485_760,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    return logger


# Create application logger
logger = setup_logger(
    name="fastapi_app",
    log_level=logging.INFO,
    log_dir="logs"
)

# Optional: Create separate loggers for different modules
database_logger = setup_logger(
    name="fastapi_app.database",
    log_level=logging.DEBUG,
    log_dir="logs"
)

service_logger = setup_logger(
    name="fastapi_app.service",
    log_level=logging.INFO,
    log_dir="logs"
)

controller_logger = setup_logger(
    name="fastapi_app.controller",
    log_level=logging.INFO,
    log_dir="logs"
)


__all__ = ["logger", "database_logger", "service_logger", "controller_logger", "setup_logger"]
