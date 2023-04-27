"""
This script generates a set of fixtures for a sales table in a database, simulating data that would be manipulated by a change data capture (CDC) system. 
The script creates JSON-formatted test data that can be used to simulate the behavior of the CDC system, enabling developers to test and debug the system with realistic data without affecting the production database.

In order to use this script, you don't need any special setup. Just make sure you have the required libraries installed (Faker) and run the script. It will generate a JSON file called "demo-cdc.json" containing the fixture data.
"""

import json
import random
import sys
from datetime import datetime
from faker import Faker

def generate_fixtures(num_fixtures, table_name, schema):
    faker = Faker()
    fixtures = {table_name: []}

    for _ in range(num_fixtures):
        record = {
            "key": random.randint(1, 1000),
            "value": {
                "payload": {
                    "after": {
                        field["field"]: faker.format(field["fake_format"]) if field.get("fake_format") else random.randint(1, 100)
                        for field in schema
                    },
                    "before": None,
                    "op": "r",
                    "source": {},  # Add source fields if needed
                    "transaction": None,
                    "ts_ms": int(datetime.now().timestamp() * 1000)
                },
                "schema": {
                    "fields": [
                        {
                            "field": field["field"],
                            "optional": field["optional"],
                            "type": field["type"]
                        }
                        for field in schema
                    ],
                    "name": f"resource_7109_171736.public.{table_name}.Envelope",
                    "optional": False,
                    "type": "struct"
                }
            }
        }
        fixtures[table_name].append(record)

    return fixtures

def main():
    num_fixtures = 3  # Set the desired number of fixtures
    table_name = "sales"
    schema = [
        {"field": "customer_id", "optional": True, "type": "int32"},
        {"field": "customer_email", "optional": True, "type": "string", "fake_format": "email"},
        {"field": "product_id", "optional": True, "type": "int32"},
        {"field": "quantity", "optional": True, "type": "int32"},
        {"field": "price", "optional": True, "type": "float"},
        {"field": "order_date", "optional": True, "type": "timestamp", "fake_format": "date"},
        {"field": "postal_code", "optional": True, "type": "string", "fake_format": "postcode"},
        {"field": "state", "optional": True, "type": "string", "fake_format": "state_abbr"},
        {"field": "customer_review", "optional": True, "type": "string", "fake_format": "text"},
        {"field": "extra_id", "optional": True, "type": "int32"},
        {"field": "order_id", "optional": True, "type": "int32"}
    ]

    fixtures = generate_fixtures(num_fixtures, table_name, schema)

    with open("./fixtures/demo-cdc.json", "w") as outfile:
        json.dump(fixtures, outfile, indent=2)

if __name__ == "__main__":
    main()
