"""
This module provides sentiment analysis functionality for the sales records in our dataset using the TextBlob library. It calculates sentiment scores for the customer reviews and adds the scores to the payload of the incoming sales records. This helps enrich the sales data with additional insights that can be used for various analytics purposes.

The module relies on the TextBlob library for Python to perform sentiment analysis. To set up this file, make sure you have the TextBlob library installed in your project environment. You can install it using pip:

pip install textblob

Additionally, you might need to download the required NLTK corpora if it's not already downloaded. You can do this by running the following command in your Python environment:

python -m textblob.download_corpora

This module includes the following function:

enrich_with_sentiment_score: Calculates the sentiment score for the customer_review field in the payload using TextBlob, and adds the calculated sentiment score to the payload.

The main purpose of this module is to add additional insights to the sales data by analyzing customer reviews, allowing the Meroxa data streaming app to generate more valuable information for further processing and analytics.
"""

from textblob import TextBlob

def enrich_with_sentiment_score(payload):
    if "customer_review" in payload and payload["customer_review"] is not None:
        review = payload["customer_review"]
        sentiment = TextBlob(review).sentiment.polarity
        payload["sentiment_score"] = sentiment
    else:
        payload["sentiment_score"] = None
