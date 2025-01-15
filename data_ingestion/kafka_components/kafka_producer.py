from kafka import KafkaProducer
from kafka.errors import KafkaError

from helper_functions import env

producer = KafkaProducer(
    bootstrap_servers=env.get_env("KAFKA_SERVER"),
    value_serializer=lambda v: v.encode('utf-8')
)

def push_log_to_kafka(log):
    producer.send(env.get_env("KAFKA_TOPIC"), value=log);