import random
from tqdm import tqdm
from faker import Faker
import pandas as pd

from data_ingestion.kafka_components import kafka_producer
from helper_functions import env
from helper_functions import logger

logger.log.info("Kafka producer connected to server")

faker = Faker()

message_levels = {
    "INFO": [
        # General System Info
        "Scheduled backup completed successfully",
        "System boot completed",
        "Database query executed in 0.015 seconds",
        "File transfer completed: 100MB sent",
        "Service restarted successfully",
        "System health check passed",
        "Number of active users: 150",
        "Response time for API endpoint: 120ms",
        
        # Server and Application Info
        "User authentication succeeded for user: admin",
        "Cache cleared successfully on server node 3",
        "SSL certificate renewed successfully",
        "New connection established from IP: 192.168.1.101",
        "Email sent to user@example.com",
        "New user registered: user123",
        "Configuration file loaded without errors",
        "Service 'nginx' restarted successfully",
        "Container 'app_server' started on Docker host",
        
        # Network Info
        "VPN connection established from remote IP: 203.0.113.5",
        "Firewall rules updated successfully",
        "Network interface eth0 assigned new IP: 10.0.0.15",
        
        # Cloud & DevOps Info
        "Autoscaling event: New EC2 instance launched",
        "Deployment pipeline completed without errors",
        "Kubernetes pod 'web-app-5d6b7f8' running",
    ],
    
    "WARN": [
        # Disk & Memory Warnings
        "Disk cleanup recommended: Temporary files exceeding threshold",
        "Bandwidth utilization exceeded 90%",
        "Network latency exceeds acceptable limit",
        "High memory usage detected on server node 4",
        "CPU temperature nearing safe limit: 75°C",
        "Unusual spike in transaction volume detected",
        "Log file size approaching limit on /var/log/syslog",
        
        # Web App Warnings
        "Slow response time detected on /api/v1/orders",
        "Deprecated API endpoint accessed by client",
        "JWT token expiring soon for user: user123",
        "Multiple failed login attempts detected for user: admin",
        
        # System & Security Warnings
        "SSH login attempt from unknown IP: 198.51.100.23",
        "Firewall rule mismatch detected in configuration",
        "Failed to sync time with NTP server",
        "Unusual traffic pattern detected on port 443",
        "High number of 404 errors detected on web server",
        
        # Cloud & DevOps Warnings
        "Kubernetes pod 'api-server' restarted unexpectedly",
        "Docker container 'db_service' using excessive memory",
        "Low free space on EBS volume attached to instance i-0abcd1234"
    ],
    
    "ERROR": [
        # Disk & Memory Errors
        "Failed to allocate memory for process ID 4567",
        "Disk read error on partition /dev/sda1",
        "Service endpoint returned HTTP 500",
        "Connection timed out while connecting to database",
        "Unable to connect to SMTP server at smtp.example.com",
        "Database replication lag exceeds threshold on replica node",
        "Error writing to disk on /var/data",
        
        # Server & Application Errors
        "Service 'nginx' failed to start due to missing config file",
        "Failed to authenticate user: invalid credentials",
        "Application error: NullPointerException in module UserAuth",
        "API rate limit exceeded for IP: 203.0.113.25",
        "Database deadlock detected on transaction ID 987654",
        "Failed to mount NFS share at /mnt/shared",
        "Email delivery failed: SMTP 554 Transaction failed",
        
        # Network & Security Errors
        "SSH connection refused from IP: 198.51.100.12",
        "DNS resolution failed for host: api.example.com",
        "SSL handshake failed with client 192.0.2.15",
        "Failed to apply firewall rules on host server01",
        "Unauthorized API access attempt detected from IP: 10.0.0.200",
        
        # Cloud & DevOps Errors
        "Docker container 'web-app' crashed due to out-of-memory error",
        "Kubernetes deployment 'backend-service' failed: ImagePullBackOff",
        "EC2 instance i-0abcd1234 terminated unexpectedly",
        "Failed to create S3 bucket: Bucket name already exists"
    ],
    
    "CRITICAL": [
        # Disk, System, & Hardware Failures
        "Disk space critically low on /dev/sdb1",
        "System reboot initiated unexpectedly due to kernel panic",
        "Unauthorized access attempt detected on port 22",
        "Malware scan detected infected file: trojan.exe in /usr/bin",
        "Root access granted to unauthorized user: hacker123",
        "Power supply unit failure detected in rack A",
        "Overheating detected in data center zone B: Temperature at 90°C",
        "Filesystem corruption detected on /var/lib/docker",
        
        # Server & Application Failures
        "Critical service 'postgresql' has stopped unexpectedly",
        "Application crash detected: segmentation fault in core module",
        "Data corruption detected in database table 'orders'",
        "Critical configuration file missing: /etc/nginx/nginx.conf",
        "Backup failed: Unable to write to remote storage",
        
        # Network & Security Breaches
        "DDoS attack detected from multiple IP addresses",
        "Firewall breach detected: Unauthorized port scan from 192.0.2.45",
        "VPN server compromised: Immediate action required",
        "Ransomware activity detected on server node 5",
        
        # Cloud & DevOps Critical Failures
        "Kubernetes cluster unreachable: API server down",
        "Cloud database instance i-db12345 unresponsive",
        "Critical AWS IAM policy misconfiguration detected",
        "Loss of quorum detected in distributed system cluster",
        "Critical failure in CI/CD pipeline: Deployment halted"
    ]
}
logs = []

# Generate synthetic raw logs as strings
def generate_logs(log_count=10):
    log_type=env.get_env("LOG_TYPE")
    services = ["cloudwatch", "grafana", "prometheus"]
    
    for _ in tqdm(range(log_count), desc="Generating synthetic logs"):
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

        logs.append(log)
        kafka_producer.push_log_to_kafka(log)

    pd.DataFrame(logs).to_csv('synthetic_logs.csv', index=False)