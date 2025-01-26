import sys
import os

# Add the project root directory to sys.path
root_path = os.path.abspath(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

print(sys.path)

from helper_functions import env, logger
logger.log.info("AlertOps AI Application Started Successfully")

from data_ingestion import generate_synthetic_logs
from data_ingestion.kafka_components import kafka_consumer

if (env.get_env("GENERATE_SYNTHETIC_LOGS")):
    generate_synthetic_logs.generate_logs(2500000)

kafka_consumer.consume_logs()