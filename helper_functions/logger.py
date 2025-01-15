import logging

def setup_logger():
    # Configurations
    logging.basicConfig(
        format="%(levelname)s: %(message)s: %(asctime)s", 
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M"
    )

    logger = logging.getLogger(__name__)
    return logger

log = setup_logger()