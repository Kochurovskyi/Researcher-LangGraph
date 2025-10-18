"""Logging configuration for the research agent."""
import logging
import sys
from config import LOG_LEVEL


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger for the research agent
    logger = logging.getLogger("research_agent")
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
    
    return logger


# Initialize logger
logger = setup_logging()

