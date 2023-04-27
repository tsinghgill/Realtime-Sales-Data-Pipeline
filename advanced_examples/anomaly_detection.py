"""
This module provides an anomaly detection mechanism for the sales records in our dataset. It uses the Isolation Forest algorithm from the scikit-learn library to identify anomalous transactions in the data. The anomaly detector takes into consideration the transaction amount, which is calculated as the product of the price and quantity of the sold items.

To set up this file, make sure to have scikit-learn installed in your project environment. You can install it using pip:

pip install scikit-learn

This module includes the following components:

generate_history_data: Generates historical sales data for training the anomaly detector.
AnomalyDetector: A wrapper class around the IsolationForest algorithm that initializes, trains, and predicts anomalies.
calculate_transaction_amount: Calculates the transaction amount from a sales record.
init_anomaly_detector: Initializes and trains the anomaly detector with historical data.

The main purpose of this module is to detect anomalies in the sales transactions to identify potentially fraudulent activities or data entry errors.
"""

from sklearn.ensemble import IsolationForest
import numpy as np
import random

def generate_history_data(num_records):
    history_data = []
    for _ in range(num_records):
        price = random.uniform(1, 50)  # Random price between 1 and 50
        quantity = random.randint(1, 10)  # Random quantity between 1 and 10
        history_data.append({"price": price, "quantity": quantity})
    return history_data

class AnomalyDetector:
    def __init__(self, contamination=0.1):
        self.detector = IsolationForest(contamination=contamination)

    def fit(self, data):
        self.detector.fit(data)

    def predict(self, data_point):
        reshaped_data = np.array(data_point).reshape(1, -1)
        return self.detector.predict(reshaped_data)[0]

def calculate_transaction_amount(payload):
    return payload['price'] * payload['quantity']

def init_anomaly_detector(history_data):
    transaction_amounts = [calculate_transaction_amount(data) for data in history_data]
    transaction_amounts = np.array(transaction_amounts).reshape(-1, 1)

    anomaly_detector = AnomalyDetector()
    anomaly_detector.fit(transaction_amounts)
    return anomaly_detector
