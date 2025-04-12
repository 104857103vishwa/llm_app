import os
from dotenv import load_dotenv

# LOGGER

import logging_config
import logging

logger = logging.getLogger(__name__)

def retreive_value( param ):
    load_dotenv()
    data = os.getenv( param )
    if not data or not param.strip():
        print(f"Warning: env with value '{ param }' missing or empty.")
        # logger.warning(f"Warning: env with value '{ param }' missing or empty.")
        return None
    return data

