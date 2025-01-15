import random
from faker import Faker

from data_ingestion.kafka_components import kafka_producer
# from helper_functions import logger

faker = Faker()

# Generate synthetic raw logs as strings
def generate_logs(log_count=10):
    services = ["cloudwatch", "grafana", "prometheus"]
    levels = ["INFO", "WARN", "ERROR", "DEBUG", "CRITICAL"]
    messages = [
        "CPU usage exceeded threshold",
        "Disk space critically low",
        "Service unavailable",
        "High memory usage detected",
        "Connection timed out",
        "Successful API request",
        "Error writing to disk",
        "Alert triggered for disk I/O"
    ]
    
    for _ in range(log_count):
        log = (
            f"[{faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')}] " 
            f"{random.choice(levels)} " 
            f"{random.choice(services)}: "
            f"{random.choice(messages)}"
        )
        kafka_producer.push_log_to_kafka(log)
