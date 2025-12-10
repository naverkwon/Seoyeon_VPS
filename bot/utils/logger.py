import logging

def setup_logger():
    """Configures the root logger and specific library loggers."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    # Debug Telegram Updates for verification
    logging.getLogger("telegram").setLevel(logging.DEBUG)
    
    return logging.getLogger(__name__)

logger = setup_logger()
