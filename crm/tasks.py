from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    graphql_endpoint = "http://localhost:8000/graphql/"
    query = """
    query {
      totalCustomers
      totalOrders
      totalRevenue
    }
    """

    try:
        response = requests.post(graphql_endpoint, json={'query': query})
        data = response.json()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = "/tmp/crm_report_log.txt"

        with open(log_path, "a") as log:
            log.write(f"\n{timestamp} - Running Weekly CRM Report\n")

            if response.status_code == 200 and "data" in data:
                stats = data["data"]
                customers = stats.get("totalCustomers", 0)
                orders = stats.get("totalOrders", 0)
                revenue = stats.get("totalRevenue", 0)

                log.write(f"Report: {customers} customers, {orders} orders, {revenue} revenue\n")
            else:
                log.write(f"Error fetching data: {data}\n")

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log:
            log.write(f"Error running report: {str(e)}\n")
