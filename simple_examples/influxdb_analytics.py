"""
This module provides functionality to write sales records to InfluxDB, a time-series database that is well-suited for real-time analytics and monitoring. Storing the sales data in InfluxDB allows us to perform time-based queries and visualizations, helping us understand sales trends and make better business decisions.

To set up this file, you need to have an InfluxDB account with a bucket and an API token. You can sign up for an account on InfluxDB's website (https://www.influxdata.com/). Set the following environment variables with the corresponding values from your InfluxDB account: INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_URL, and INFLUXDB_BUCKET.

This module includes the following function:

write_data_to_influxdb: Takes a payload dictionary representing a sales record and writes it to InfluxDB as a time-series point. The function creates a Point object with the sales data, tags, and fields, and then uses the InfluxDB write API to write the point to the specified bucket and organization.

By storing the sales data in InfluxDB, we can take advantage of its powerful time-series analysis capabilities to perform real-time analytics and monitoring. This can help us identify trends, detect anomalies, and optimize our sales operations based on historical patterns and current conditions.
"""


# Go to influxdata.com in the sales-demo bucket
# SELECT * FROM "sales_data"

import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import Dict

token = os.getenv("INFLUXDB_TOKEN")
org = "sales-demo"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
bucket = "sales-demo"

write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

def write_data_to_influxdb(payload: Dict):
    point = (
        Point("sales_data")
        .tag("customer_id", payload['customer_id'])
        .tag("customer_email", payload['customer_email'])
        .tag("product_id", payload['product_id'])
        .field("quantity", payload['quantity'])
        .field("price", payload['price'])
        .field("order_date", payload['order_date'])
        .field("postal_code", payload['postal_code'])
        .field("state", payload['state'])
        .field("customer_review", payload['customer_review'])
    )
    write_api.write(bucket=bucket, org=org, record=point)
