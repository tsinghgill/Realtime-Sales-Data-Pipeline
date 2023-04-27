import logging
import sys
import sentry_sdk

from turbine.runtime import RecordList
from turbine.runtime import Runtime

# Import enrichment and utility functions
from simple_examples.geolocation_enrichment import enrich_with_geolocation
from simple_examples.tax_enrichment import enrich_with_tax_rate
from simple_examples.email_hashing import enrich_with_hashed_email
from simple_examples.filtering import remove_unnecessary_fields
from simple_examples.influxdb_analytics import write_data_to_influxdb
from simple_examples.sentry_monitoring import init_sentry

# Import advanced examples
from advanced_examples.anomaly_detection import init_anomaly_detector, calculate_transaction_amount, generate_history_data
from advanced_examples.sentiment_analysis import enrich_with_sentiment_score
from advanced_examples.schema_validation import validate_payload
from advanced_examples.redis_deduplication import create_redis_client, is_duplicate

# Initialize Sentry for error monitoring
init_sentry()
# Create a Redis client for deduplication
redis_client = create_redis_client()

# Generate historical data for anomaly detection
history_data = generate_history_data(1000)
anomaly_detector = init_anomaly_detector(history_data)

# Set up logging
logging.basicConfig(level=logging.INFO)

def transform(records: RecordList) -> RecordList:
    logging.info(f"processing {len(records)} record(s)")

    for record in records:
        logging.info(f"input: {record}")
        try:
            payload = record.value["payload"]["after"]

            # Validate payload schema
            if not validate_payload(payload):
                print(f"Invalid schema for record: {record}")
                continue

            # Data deduplication
            dedup_key = f"{payload['customer_id']}_{payload['order_id']}"
            if is_duplicate(redis_client, dedup_key):
                print(f"Duplicate record found: {record.key}")
                continue

            # Enrich with geolocation
            enrich_with_geolocation(payload)

            # Enrich with tax rate
            enrich_with_tax_rate(payload)

            # Hash customer email
            enrich_with_hashed_email(payload)

            # Remove unnecessary fields
            remove_unnecessary_fields(payload, ["extra_id"])

            # Write data to InfluxDB for Analytics
            write_data_to_influxdb(payload)

            # Detect anomalies
            transaction_amount = calculate_transaction_amount(payload)
            is_anomaly = anomaly_detector.predict(transaction_amount) == -1
            payload["is_anomaly"] = "true" if is_anomaly else "false"

            # Enrich with sentiment analysis
            enrich_with_sentiment_score(payload)

            logging.info(f"output: {record}")
        except Exception as e:
            print("Error occurred while parsing records: " + str(e))
            logging.info(f"output: {record}")
            # Capture the exception using Sentry
            sentry_sdk.capture_exception(e)
    return records



class App:
    @staticmethod
    async def run(turbine: Runtime):
        try:
            source = await turbine.resources("source_name")

            records = await source.records("sales", {})

            turbine.register_secrets("GOOGLE_MAPS_API_KEY")
            turbine.register_secrets("INFLUXDB_TOKEN")
            turbine.register_secrets("SENTRY_DSN")
            turbine.register_secrets("REDIS_HOST")
            turbine.register_secrets("REDIS_PORT")
            turbine.register_secrets("REDIS_PASSWORD")

            transformed = await turbine.process(records, transform)

            destination_db = await turbine.resources("destination_name")

            await destination_db.write(transformed, "collection_archive", {})
        except Exception as e:
            print(e, file=sys.stderr)
