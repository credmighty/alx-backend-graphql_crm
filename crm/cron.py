from django-cron import CronJobBase, Schedule
from datetime import datetime

def log_crm_heartbeat():
    """
    Logs a heartbeat message to /tmp/crm_heartbeat.log.txt
    in the format: DD/MM/YYYY-HH:MM:SS CRM is alive
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_msg = f"{timestamp} CRM is alive"

    log_file = "/tmp/crm_heartbeat_log.txt"

    with open(log_file, "a") as doc:
        doc.write(log_msg)
