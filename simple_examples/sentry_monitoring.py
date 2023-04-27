"""
This module provides functionality to initialize Sentry, an error and performance monitoring tool, for our data transformation pipeline. Integrating Sentry into our pipeline helps us track errors and performance issues that may occur during the transformation process, allowing us to identify and fix problems more efficiently. By monitoring our pipeline with Sentry, we can improve the reliability and performance of our data processing operations.

To set up this file, you need to have a Sentry account and obtain a Sentry DSN (Data Source Name) for your project. You can sign up for a Sentry account at https://sentry.io/. After creating a project in Sentry, you will be provided with a DSN. Set the SENTRY_DSN environment variable with the value from your Sentry account.

This module includes the following function:

init_sentry: Initializes Sentry with the provided DSN and sets the traces_sample_rate. The traces_sample_rate determines the percentage of requests that Sentry will capture for performance monitoring. In this example, we've set the rate to 0.5, meaning that Sentry will capture 50% of the requests.

By integrating Sentry into our data transformation pipeline, we can monitor errors and performance issues in real-time, allowing us to quickly identify and fix problems that may arise. This helps improve the reliability and performance of our data processing operations and ensures that our transformed sales data is accurate and up-to-date.
"""

import os
import sentry_sdk

SENTRY_DSN = os.getenv("SENTRY_DSN")

def init_sentry():
    sentry_sdk.init(SENTRY_DSN, traces_sample_rate=0.5)
