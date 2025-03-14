import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import get_settings

settings = get_settings()


def setup_logging(log_file: str = "logs/globetrotter.log") -> None:
    """Configure logging with rotating file handler."""
    # Create logs directory if it doesn't exist
    log_path = Path(log_file).parent
    log_path.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger("globetrotter")
    logger.setLevel(settings.LOG_LEVEL)

    # Create formatters
    formatter = logging.Formatter(settings.LOG_FORMAT)

    # Create and configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(settings.LOG_LEVEL)

    # Create and configure file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=500 * 1024 * 1024,  # 500MB
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(settings.LOG_LEVEL)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Configure uvicorn logging
    for name in logging.root.manager.loggerDict:
        if name.startswith("uvicorn"):
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.handlers = []
            uvicorn_logger.addHandler(console_handler)
            uvicorn_logger.addHandler(file_handler)

    logger.info("Logging configuration completed")


logger = logging.getLogger("globetrotter")
