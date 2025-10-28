#!/usr/bin/env python3

"""
Description:
This script queries the GraphQL endpoint for orders made in the last 7 days.
It logs each order’s ID and customer email to /tmp/order_reminders_log.txt
and prints a message when done.
"""

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# --- Configuration ---
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Setup GraphQL client ---
transport = RequestsHTTPTransport(
    url=GRAPHQL_ENDPOINT,
    verify=False,
    retries=3,
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# --- Define time range ---
seven_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()

# --- GraphQL Query ---
query = gql(f"""
query {{
  orders(filter: {{ orderDate_Gte: "{seven_days_ago}" }}) {{
    id
    customer {{
      email
    }}
  }}
}}
""")

# --- Execute query ---
response = client.execute(query)

# --- Log the results ---
orders = response.get("orders", [])
with open(LOG_FILE, "a") as log:
    for order in orders:
        order_id = order["id"]
        customer_email = order["customer"]["email"]
        log.write(f"[{TIMESTAMP}] Order ID: {order_id}, Customer Email: {customer_email}\n")

print("Order reminders processed!")
