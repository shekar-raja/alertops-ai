import os
from dotenv import load_dotenv
from helper_functions import logger

environment = os.getenv('APP_ENV', 'dev')
env_file = os.path.join('environments', f'{environment}.env')
load_dotenv(env_file)

logger.log.info(environment + " environment")

def get_env(name):
    variable = os.getenv(name)
    return variable