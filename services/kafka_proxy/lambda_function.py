import json
import pendulum
import os
from kafka_client import KafkaProducerClient

def lambda_handler(event, context):
    kafka_config = {
        "bootstrap_servers" : os.environ["KAFKA_BOOTSTRAP"],
        "topic" : os.environ["KAFKA_TOPIC"],
        "sasl_username" : os.environ["KAFKA_USERNAME"],
        "sasl_password" : os.environ["KAFKA_PASSWORD"]
    }
    kafka_client = KafkaProducerClient(kafka_config)

    msg = {
        "source" : "segment",
        "type" : "test",
        "data" : event,
        "timestamp" : pendulum.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    kafka_client.send_message(json.dumps(msg))

    return {
        'statusCode': 200,
        'body': json.dumps('Send message success')
    }
