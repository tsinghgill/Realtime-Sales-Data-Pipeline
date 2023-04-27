"""
This module provides data deduplication functionality for the sales records in our dataset using Redis as a key-value store. It helps ensure that the Meroxa data streaming app only processes unique records, avoiding repeated processing of the same sales data.

The module relies on the Redis client library for Python to interact with a Redis server. To set up this file, make sure you have the Redis client library installed in your project environment. You can install it using pip:

pip install redis

Additionally, ensure that the environment variables REDIS_HOST, REDIS_PORT, and REDIS_PASSWORD are set to the appropriate values for your Redis server.

This module includes the following functions:

create_redis_client: Creates a Redis client instance using the provided host, port, and password.
is_duplicate: Checks if a deduplication key exists in Redis, and if not, sets it with an expiration time.

The main purpose of this module is to prevent duplicate sales records from being processed and to maintain data consistency within the dataset.
"""

import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

def create_redis_client():
    redis_client = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0
    )
    return redis_client


def is_duplicate(redis_client, dedup_key, expiration_time=3600):
    try:
        result = redis_client.set(
            dedup_key, "placeholder", ex=expiration_time, nx=True
        )
        return result is None
    except redis.RedisError as e:
        print(f"Error interacting with Redis: {e}")
        return False

