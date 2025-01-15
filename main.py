from helper_functions import logger
logger.log.info("AlertOps AI Application Started Successfully")

from data_ingestion import generate_synthetic_logs
from helper_functions import env
from data_ingestion.kafka_components import kafka_consumer

generate_synthetic_logs.generate_logs()

kafka_consumer.consume_logs()