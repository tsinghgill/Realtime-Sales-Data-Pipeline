"""
This module provides schema validation functionality for the sales records in our dataset using the Pydantic library. It ensures that the incoming records conform to a predefined schema, helping maintain data consistency and quality in the dataset.

The module relies on the Pydantic library for Python to perform the schema validation. To set up this file, make sure you have the Pydantic library installed in your project environment. You can install it using pip:

pip install pydantic

This module includes the following components:

SalesRecordSchema: A Pydantic BaseModel class that defines the schema for the sales records, specifying the field names, types, and other constraints.
validate_payload: A function that validates a given payload (dictionary) against the SalesRecordSchema. It returns True if the payload is valid, and False otherwise.

The main purpose of this module is to ensure that only records with valid schema are processed by the Meroxa data streaming app, thus preventing potential issues caused by incorrect or missing data fields.
"""

from pydantic import BaseModel, ValidationError

class SalesRecordSchema(BaseModel):
    customer_id: int
    customer_email: str
    product_id: int
    quantity: int
    price: float
    order_date: str
    postal_code: str
    state: str
    customer_review: str
    extra_id: int
    order_id: int

def validate_payload(payload: dict) -> bool:
    try:
        SalesRecordSchema(**payload)
        return True
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return False
