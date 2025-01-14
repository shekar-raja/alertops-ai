import logging

# Configurations
logging.basicConfig(format="%(levelname)s: %(message)s: %(asctime)s", 
                    level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M")

logging.info("AlertOps AI Application Started Successfully")