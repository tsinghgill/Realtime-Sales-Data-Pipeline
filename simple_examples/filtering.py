"""
This module provides a function to remove unnecessary fields from the sales records in our dataset. This helps reduce the size of the dataset and focuses the data processing on the most relevant information. By removing unnecessary fields, we can streamline our data processing pipeline and reduce storage and bandwidth requirements.

No additional setup is required for this file.

This module includes the following function:

remove_unnecessary_fields: Takes the payload and a list of fields to exclude. It iterates through the fields to exclude and removes them from the payload if they exist. This function helps clean up the payload, keeping only the relevant data fields.

The main purpose of this module is to remove any fields that are not essential for further processing or analysis. This helps ensure that the Meroxa data streaming app processes and stores only the necessary data, improving efficiency and reducing resource consumption. By removing unnecessary fields from the sales data, we can optimize our data processing pipeline and focus on the most important information for our analysis.
"""

def remove_unnecessary_fields(payload: dict, fields_to_exclude):
    for field in fields_to_exclude:
        if field in payload:
            del payload[field]
