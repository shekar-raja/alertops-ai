import random
from faker import Faker

from data_ingestion.kafka_components import kafka_producer
from helper_functions import env
# from helper_functions import logger

faker = Faker()

message_levels = {
    "INFO": [
        "Scheduled backup completed successfully",
        "System boot completed",
        "Database query executed in 0.015 seconds",
        "File transfer completed: 100MB sent",
        "Service restarted successfully",
        "System health check passed",
        "Number of active users: 150",
        "Response time for API endpoint: 120ms"
    ],
    "WARN": [
        "Disk cleanup recommended: Temporary files exceeding threshold",
        "Bandwidth utilization exceeded 90%",
        "Network latency exceeds acceptable limit",
        "High memory usage detected",
        "CPU temperature nearing safe limit",
        "Unusual spike in transaction volume detected"
    ],
    "ERROR": [
        "Failed to allocate memory",
        "Disk read error on partition /dev/sda1",
        "Service endpoint returned HTTP 500",
        "Connection timed out",
        "Unable to connect to SMTP server",
        "Database replication lag exceeds threshold",
        "Error writing to disk"
    ],
    "CRITICAL": [
        "Disk space critically low",
        "System reboot initiated unexpectedly",
        "Unauthorized access attempt detected",
        "Malware scan detected infected file: trojan.exe",
        "Root access granted to unauthorized user",
        "Power supply unit failure in rack A",
        "Overheating detected in data center zone B"
    ]
}

# Generate synthetic raw logs as strings
def generate_logs(log_count=10):
    log_type=env.get_env("LOG_TYPE")
    services = ["cloudwatch", "grafana", "prometheus"]
    
    for _ in range(log_count):
        timestamp = faker.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')

        # Select a random log level and corresponding message
        level = random.choice(list(message_levels.keys()))
        message = random.choice(message_levels[level])

        if log_type == "cloudwatch":
            log = (
                f"{timestamp} [{level}] "
                f"[LogGroup:{random.choice(['/aws/lambda/my-function', '/aws/ec2/my-instance'])}] "
                f"[LogStream:{faker.uuid4()}] {message}"
            )

        elif log_type == "zabbix":
            log = (
                f"{timestamp} [{level}] "
                f"Trigger: {message} "
                f"Status: Problem Host: {random.choice(['web-server-01', 'db-server-01'])}"
            )

        elif log_type == "uptimerobot":
            log = (
                f"{timestamp} Monitor: {random.choice(['MyWebsite', 'MyAPI'])} "
                f"Type: {random.choice(['HTTP', 'Keyword'])} "
                f"Status: {random.choice(['Up', 'Down'])} "
                f"{message}"
            )

        elif log_type == "grafana":
            log = (
                f"{timestamp} [{level}] "
                f"Alert: {random.choice(['High CPU Usage', 'Disk Space Low'])} "
                f"State: {random.choice(['Firing', 'Resolved'])} "
                f"Instance: {random.choice(['prod-server-01', 'prod-server-02'])} "
                f"Details: {message}"
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
                f"{timestamp} level={level.lower()} "
                f"msg=\"{message}\" "
                f"service={random.choice(['auth-server', 'web-server'])} "
                f"environment={random.choice(['staging', 'production'])}"
            )
        else:    
            log = (
                f"[{timestamp}] " 
                f"{level} " 
                f"{random.choice(services)}: "
                f"{message}"
            )

        kafka_producer.push_log_to_kafka(log)
