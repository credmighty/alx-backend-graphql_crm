from django-cron import CronJobBase, Schedule
import requests
from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import, gql, Client

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


def update_low_stock():
    graphql_endpoint = "http://localhost:8000/graphql/"

    mutation = """
    mutation {
      updateLowStockProducts {
        success
        message
        updatedProducts {
          name
          stock
        }
      }
    }
    """

    response = requests.post(graphql_endpoint, json={'query': mutation})
    data = response.json()

    log_path = "/tmp/low_stock_updates_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a") as log_file:
        log_file.write(f"\n[{timestamp}] Running Low-Stock Update Job\n")

        if response.status_code == 200 and "data" in data:
            result = data["data"]["updateLowStockProducts"]
            log_file.write(f"Message: {result['message']}\n")
            for p in result["updatedProducts"]:
                log_file.write(f"- {p['name']}: New stock = {p['stock']}\n")
        else:
            log_file.write(f"Error: {data}\n")
