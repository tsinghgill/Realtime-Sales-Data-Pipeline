"""
This module provides email hashing functionality for the sales records in our dataset. It hashes customer email addresses using the SHA-256 algorithm to anonymize personal information, enhancing data privacy and security. By hashing email addresses, we protect sensitive customer data while still allowing for unique customer identification and analysis.

The module uses Python's built-in hashlib library to perform SHA-256 hashing. No additional setup is required for this file.

This module includes the following function:

enrich_with_hashed_email: Takes the payload containing customer_email and hashes the email address using the SHA-256 algorithm. The hashed email is then used to replace the original email address in the payload.

The main purpose of this module is to improve data privacy and security in the sales data by anonymizing customer email addresses. This helps ensure that the Meroxa data streaming app complies with data protection regulations and best practices while processing and storing customer data.
"""

import hashlib

def enrich_with_hashed_email(payload):
    email = payload["customer_email"]
    hashed_email = hashlib.sha256(email.encode("utf-8")).hexdigest()
    payload["customer_email"] = hashed_email
