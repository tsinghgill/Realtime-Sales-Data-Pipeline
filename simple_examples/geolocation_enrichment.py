"""
This module provides functionality to enrich sales records with geolocation data based on the postal code of the customer. By adding geolocation information to our sales table, we can perform geospatial analysis and visualize sales patterns on a map. This can help with understanding regional trends and improve decision-making for marketing, inventory management, and other business areas.

To set up this file, you need to obtain a Google Maps API key and set it as an environment variable (GOOGLE_MAPS_API_KEY). You can get a Google Maps API key from the Google Cloud Console: https://console.cloud.google.com/apis/credentials

This module includes the following functions:

get_geolocation: Takes a postal code as input and queries the Google Maps Geocoding API to retrieve the corresponding geolocation data (latitude and longitude). Returns the geolocation data as a dictionary or None if the API call fails or the data is not available.

enrich_with_geolocation: Takes the payload and enriches it with geolocation data. It retrieves the postal code from the payload, calls the get_geolocation function, and adds the latitude and longitude to the payload if the geolocation data is available.

The main purpose of this module is to add geospatial context to our sales data by enriching it with geolocation information. This allows us to perform geospatial analysis, such as identifying regional trends, visualizing sales on a map, and optimizing delivery routes. By adding geolocation data to our sales records, we can enhance our understanding of the data and improve decision-making across various business areas.
"""

import os
import requests

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_geolocation(postal_code):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={postal_code}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            return data["results"][0]["geometry"]["location"]
    return None

def enrich_with_geolocation(payload):
    postal_code = payload["postal_code"]
    geolocation = get_geolocation(postal_code)

    if geolocation:
        payload["latitude"] = geolocation["lat"]
        payload["longitude"] = geolocation["lng"]
