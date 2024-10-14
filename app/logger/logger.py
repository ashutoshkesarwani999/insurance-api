import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.setLevel(os.environ.get("LOG_LEVEL") or logging.INFO)