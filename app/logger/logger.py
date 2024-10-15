import os
import logging
from fastapi import BackgroundTasks

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.setLevel(os.environ.get("LOG_LEVEL") or logging.INFO)

# Create a console handler and set the level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)