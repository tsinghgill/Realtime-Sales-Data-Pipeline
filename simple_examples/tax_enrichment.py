"""
This module provides functionality to enrich sales records with state-specific tax rates. By adding tax rate information to our sales table, we can calculate the total tax amount for each sale, helping us understand the tax liabilities and generate accurate financial reports for the company.

The state_tax_rates dictionary contains the tax rates for each US state. If a state is not found in the dictionary, a default tax rate of 0.0 is used. This module assumes that tax rates remain constant and doesn't account for tax rate changes over time.

This module includes the following function:

enrich_with_tax_rate: Takes a payload dictionary representing a sales record and enriches it with the tax rate for the corresponding state. It retrieves the state from the payload, looks up the tax rate in the state_tax_rates dictionary, and adds the tax rate to the payload.

By enriching our sales records with tax rate information, we can calculate the total tax amount for each sale, which is crucial for generating accurate financial reports and understanding the company's tax liabilities. This additional data allows us to better analyze the sales data and make informed business decisions.
"""

state_tax_rates = {
    "AL": 0.04,
    "AK": 0.00,
    "AZ": 0.056,
    "AR": 0.065,
    "CA": 0.0725,
    "CO": 0.029,
    "CT": 0.0635,
    "DE": 0.00,
    "FL": 0.06,
    "GA": 0.04,
    "HI": 0.04,
    "ID": 0.06,
    "IL": 0.0625,
    "IN": 0.07,
    "IA": 0.06,
    "KS": 0.065,
    "KY": 0.06,
    "LA": 0.0445,
    "ME": 0.055,
    "MD": 0.06,
    "MA": 0.0625,
    "MI": 0.06,
    "MN": 0.06875,
    "MS": 0.07,
    "MO": 0.04225,
    "MT": 0.00,
    "NE": 0.055,
    "NV": 0.0685,
    "NH": 0.00,
    "NJ": 0.06625,
    "NM": 0.05125,
    "NY": 0.04,
    "NC": 0.0475,
    "ND": 0.05,
    "OH": 0.0575,
    "OK": 0.045,
    "OR": 0.00,
    "PA": 0.06,
    "RI": 0.07,
    "SC": 0.06,
    "SD": 0.045,
    "TN": 0.07,
    "TX": 0.0625,
    "UT": 0.0595,
    "VT": 0.06,
    "VA": 0.043,
    "WA": 0.065,
    "WV": 0.06,
    "WI": 0.05,
    "WY": 0.04,
}

def enrich_with_tax_rate(payload):
    state = payload["state"]

    if state in state_tax_rates:
        tax_rate = state_tax_rates[state]
    else:
        tax_rate = 0.0  # Default tax rate if the state is not found in the dictionary

    payload["tax_rate"] = tax_rate
