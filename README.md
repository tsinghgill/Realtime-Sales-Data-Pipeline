
# Meroxa Data App: Sales Data Transformation Pipeline

## Getting Started

This repository contains a data transformation pipeline for processing and enriching sales records. The pipeline takes raw sales data, validates it, deduplicates it, and enriches it with additional information such as geolocation data, tax rates, sentiment scores, and hashed email addresses. The transformed data is then written to InfluxDB for further analysis and visualization.

```bash
$ tree sales-demo/
├── README.md
├── __init__.py
├── __pycache__
│   ├── email_hashing.cpython-310.pyc
│   ├── filtering.cpython-310.pyc
│   ├── geolocation_enrichment.cpython-310.pyc
│   ├── influxdb_analytics.cpython-310.pyc
│   ├── main.cpython-310.pyc
│   ├── main.cpython-311.pyc
│   └── tax_enrichment.cpython-310.pyc
├── advanced_examples
│   ├── __pycache__
│   │   ├── anomaly_detection.cpython-311.pyc
│   │   ├── redis_deduplication.cpython-311.pyc
│   │   ├── schema_validation.cpython-311.pyc
│   │   └── sentiment_analysis.cpython-311.pyc
│   ├── anomaly_detection.py
│   ├── redis_deduplication.py
│   ├── schema_validation.py
│   └── sentiment_analysis.py
├── app.json
├── fixtures
│   ├── demo-cdc.json
│   └── demo-no-cdc.json
├── main.py
├── requirements.txt
├── scripts
│   ├── generate_fixtures.py
│   └── pg_data_generation.py
└── simple_examples
    ├── __pycache__
    │   ├── email_hashing.cpython-311.pyc
    │   ├── filtering.cpython-311.pyc
    │   ├── geolocation_enrichment.cpython-311.pyc
    │   ├── influxdb_analytics.cpython-311.pyc
    │   ├── sentry_monitoring.cpython-311.pyc
    │   └── tax_enrichment.cpython-311.pyc
    ├── email_hashing.py
    ├── filtering.py
    ├── geolocation_enrichment.py
    ├── influxdb_analytics.py
    ├── sentry_monitoring.py
    └── tax_enrichment.py
```

This will be a full-fledged Turbine app that can run. You can even run the tests using the command `meroxa apps run` in the root of the app directory. It provides just enough to show you what you need to get started.

### Requirements

Before you start, make sure you have the following:

- Python 3.8 or higher
- A Redis instance
- A Google Maps API key
- An InfluxDB account with a bucket and API token
- A Sentry account with a DSN (Data Source Name)

### Installation

1. `pip install -r requirements.txt`
2. Generate fixtures `python scripts/generate_fixtures`
3. Export secrets:
      POSTGRES_CONN_URL=<YOUR_SECRET>
      GOOGLE_MAPS_API_KEY=<YOUR_SECRET>
      INFLUXDB_TOKEN=<YOUR_SECRET>
      SENTRY_DSN=<YOUR_SECRET>
      REDIS_HOST=<YOUR_SECRET>
      REDIS_PORT=<YOUR_SECRET>
      REDIS_PASSWORD=<YOUR_SECRET>
4. Run the app `meroxa apps run`

## Meroxa + Turbine Developer Journey

This configuration file is where you begin your Turbine journey. Any time a Turbine app runs, this is the entry point for the entire application. When the project is created, the file will look like this:

```python
# Dependencies of the example data app
import hashlib
import sys

from turbine.runtime import RecordList, Runtime as Turbine

def anonymize(records: RecordList) -> RecordList:
    for record in records:
        try:
            payload = record.value["payload"]

            # Hash the email
            payload["customer_email"] = hashlib.sha256(
                payload["customer_email"].encode("utf-8")
            ).hexdigest()

        except Exception as e:
            print("Error occurred while parsing records: " + str(e))
    return records


class App:
    @staticmethod
    async def run(turbine: Turbine):
      try:
        source = await turbine.resources("source_name")

        records = await source.records("collection_name")

        anonymized = await turbine.process(records, anonymize)

        destination_db = await turbine.resources("destination_name")

        await destination_db.write(anonymized, "collection_archive")
      except Exception as e:
          print(e, file=sys.stderr)
```

Let's talk about the important parts of this code. Turbine apps have five functions that comprise the entire DSL. Outside of these functions, you can write whatever code you want to accomplish your tasks:

```python
async def run(turbine: Turbine):
```

`run` is the main entry point for the application. This is where you can initialize the Turbine framework. This is also the place where, when you deploy your Turbine app to Meroxa, Meroxa will use this as the place to boot up the application.

```python
source = await turbine.resources("source_name")
```

The `resources` function identifies the upstream or downstream system that you want your code to work with. The `source_name` is the string identifier of the particular system. The string should map to an associated identifier in your `app.json` to configure what's being connected to. For more details, see the `app.json` section.

```python
records = await source.records("collection_name")
```

Once you've got `resources` set up, you can now stream records from it, but you need to identify what records you want. The `records` function identifies the records or events that you want to stream into your data app.

```python
anonymized = await turbine.process(records, anonymize)
```

The `process` function is Turbine's way of saying, for the records that are coming in, I want you to process these records against a function. Once your app is deployed on Meroxa, Meroxa will do the work to take each record or event that does get streamed to your app and then run your code against it. This allows Meroxa to scale out your processing relative to the velocity of the records streaming in.

```python
await destination_db.write(anonymized, "collection_archive")
```

The `write` function is optional. It takes any records given to it and streams them to the downstream system. In many cases, you might not need to stream data to another system, but this gives you an easy way to do so.


### `app.json`

This file contains all of the options for configuring a Turbine app. Upon initialization of an app, the CLI will scaffold the file for you with available options:

```json
{
  "name": "testapp",
  "language": "python",
  "environment": "common",
  "resources": {
    "source_name": "fixtures/demo-cdc.json"
  }
}
```

* `name` - The name of your application. This should not change after app initialization.
* `language` - Tells Meroxa what language the app is upon deployment.
* `environment` - "common" is the only available environment. Meroxa does have the ability to create isolated environments but this feature is currently in beta.
* `resources` - These are the named integrations that you'll use in your application. The `source_name` needs to match the name of the resource that you'll set up in Meroxa using the `meroxa resources create` command or via the Dashboard. You can point to the path in the fixtures that'll be used to mock the resource when you run `meroxa apps run`.

### Fixtures

Fixtures are JSON-formatted samples of data records you can use while locally developing your Turbine app. Whether CDC or non-CDC-formatted data records, fixtures adhere to the following structure:

```json
{
  "collection_name": [
    {
      "key": "1",
      "value": {
  		  "schema": {
  			  /* ... */
  		  },
  		  "payload": {
  			  /* ... */
  		  }
      }
    }
  ]
}
```
* `collection_name` — Identifies the name of the records or events you are streaming to your data app.
* `key` — Denotes one or more sample records within a fixture file. `key` is always a string.
* `value` — Holds the `schema` and `payload` of the sample data record.
* `schema` — Comes as part of your sample data record. `schema` describes the record or event structure.
* `payload` — Comes as part of your sample data record. `payload` describes what about the record or event changed.

Your newly created data app should have a `demo-cdc.json` and `demo-non-cdc.json` in the `/fixtures` directory as examples to follow.

### Testing

Testing should follow standard Python development practices.

## Documentation && Reference

The most comprehensive documentation for Turbine and how to work with Turbine apps is on the Meroxa site: [https://docs.meroxa.com/](https://docs.meroxa.com)

## Example apps

[See what a sample python data app looks like using our framework](https://github.com/meroxa/turbine-py-examples)
