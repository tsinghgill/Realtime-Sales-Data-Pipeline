"""
This script is used to generate and insert sample data into the 'sales' table in a PostgreSQL database. 
It leverages the Faker library to create realistic data for various fields, such as customer email, product ID, quantity, price, order date, postal code, state, and customer review. 
The script creates a table called 'sales' if it does not exist and inserts 20 records with randomly generated data. This helps developers work with realistic data when testing and debugging applications that interact with the sales table.

To set up and use this script, make sure you have the required libraries installed (psycopg and Faker), and provide the correct PostgreSQL connection URL as an environment variable (POSTGRES_CONN_URL). 
After setting up the environment, you can run the script, and it will create the 'sales' table if it doesn't exist and populate it with 20 rows of sample data.
"""

#!/usr/bin/python

import os
import psycopg
from faker import Faker

# Connect to the PostgreSQL database
conn = psycopg.connect(conninfo=os.getenv("POSTGRES_CONN_URL"))

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create an instance of the Faker class
faker = Faker()

# Create the 'sales' table if it does not exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS sales (
	    id SERIAL PRIMARY KEY,
	    customer_id INTEGER NOT NULL,
	    customer_email CHARACTER VARYING (100) NOT NULL,
	    product_id INTEGER NOT NULL,
	    quantity INTEGER NOT NULL,
	    price DOUBLE PRECISION NOT NULL,
	    order_date TIMESTAMP NOT NULL,
	    postal_code CHARACTER VARYING (10) NOT NULL,
	    state CHARACTER VARYING (2) NOT NULL,
	    customer_review CHARACTER VARYING (255),
        extra_id INTEGER NOT NULL,
        order_id INTEGER NOT NULL
    )"""
)

# Use a loop to generate multiple records for sales table
for _ in range(20):
    # Use the Faker class to generate data
    customer_id = faker.random_int(min=1, max=100)
    customer_email = faker.email()
    product_id = faker.random_int(min=1, max=10)
    quantity = faker.random_int(min=1, max=5)
    price = faker.random_number(digits=2)
    order_date = faker.date_time()
    postal_code = faker.postcode()
    state = faker.state_abbr()
    customer_review = faker.text(max_nb_chars=200)
    extra_id = faker.random_int(min=1, max=10)
    order_id = faker.random_int(min=1, max=10)

    # Execute an SQL INSERT command, passing in the generated data as values
    cursor.execute(
        f"INSERT INTO sales (customer_id, customer_email, product_id, quantity, price, order_date, postal_code, state, customer_review, extra_id, order_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            customer_id,
            customer_email,
            product_id,
            quantity,
            price,
            order_date,
            postal_code,
            state,
            customer_review,
            extra_id,
            order_id,
        ),
    )

# Commit the changes to the database
conn.commit()
