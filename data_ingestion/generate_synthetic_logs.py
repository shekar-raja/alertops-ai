import random
from faker import Faker

from data_ingestion.kafka_components import kafka_producer
from helper_functions import env
# from helper_functions import logger

faker = Faker()

# Generate synthetic raw logs as strings
def generate_logs(log_count=10):
    log_type=env.get_env("LOG_TYPE")
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
        timestamp = faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')

        if log_type == "cloudwatch":
            log = (
                f"{timestamp} [{random.choice(['INFO', 'ERROR'])}] "
                f"[LogGroup:{random.choice(['/aws/lambda/my-function', '/aws/ec2/my-instance'])}] "
                f"[LogStream:{faker.uuid4()}] {random.choice(['Request completed successfully.', 'CPU usage exceeded 90%.'])}"
            )

        elif log_type == "zabbix":
            log = (
                f"{timestamp} [{random.choice(['High', 'Critical'])}] "
                f"Trigger: {random.choice(['Disk space low on /dev/sda1', 'MySQL service down'])} "
                f"Status: Problem Host: {random.choice(['web-server-01', 'db-server-01'])}"
            )

        elif log_type == "uptimerobot":
            log = (
                f"{timestamp} Monitor: {random.choice(['MyWebsite', 'MyAPI'])} "
                f"Type: {random.choice(['HTTP', 'Keyword'])} "
                f"Status: {random.choice(['Up', 'Down'])} "
                f"{random.choice(['Duration: 5 minutes', 'ResponseTime: 200ms'])}"
            )

        elif log_type == "grafana":
            log = (
                f"{timestamp} [{random.choice(['Alerting', 'OK'])}] "
                f"Alert: {random.choice(['High CPU Usage', 'Disk Space Low'])} "
                f"State: {random.choice(['Firing', 'Resolved'])} "
                f"Instance: {random.choice(['prod-server-01', 'prod-server-02'])} "
                f"Details: {random.choice(['CPU usage exceeded 85%', 'Disk space below 15%'])}"
            )

        # elif log_type == "prometheus":
        #     log = (
        #         f"{timestamp} Metric: {random.choice(['http_requests_total', 'cpu_usage'])} "
        #         f"Value: {round(random.uniform(50, 100), 2)} "
        #         f"Labels: {random.choice(['{method=\"GET\", status=\"200\", instance=\"web-server-01\"}', "
        #         f"'{instance=\"db-server-01\", environment=\"production\"}'])}"
        #     )
        elif log_type == "loki":
            log = (
                f"{timestamp} level={random.choice(['info', 'error'])} "
                f"msg=\"{random.choice(['Service unavailable', 'Request processed successfully'])}\" "
                f"service={random.choice(['auth-server', 'web-server'])} "
                f"environment={random.choice(['staging', 'production'])}"
            )
        else:    
            log = (
                f"[{timestamp}] " 
                f"{random.choice(levels)} " 
                f"{random.choice(services)}: "
                f"{random.choice(messages)}"
            )

        kafka_producer.push_log_to_kafka(log)
