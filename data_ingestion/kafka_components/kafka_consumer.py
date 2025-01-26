from kafka import KafkaConsumer

from helper_functions import env
from helper_functions import logger

logs = []

def consume_logs():
    logger.log.info("Kafka consumer connected to server")
    consumer = KafkaConsumer(
        env.get_env("KAFKA_TOPIC"),
        bootstrap_servers=env.get_env("KAFKA_SERVER"),
        enable_auto_commit=True,
        group_id='log-consumer-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    try:
        for message in consumer:
            # print(f"Received log: {message.value}")
            logs.append(message.value)
    except KeyboardInterrupt:
        logger.log.info("Kafka consumer stopped.")
    finally:
        consumer.close()
        logger.log.info("Kafka consumer closed.")

if __name__ == "__main__":
    consume_logs()