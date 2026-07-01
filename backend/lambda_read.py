import json
import boto3
from boto3.dynamodb.conditions import Key
import time

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("FEC_SensorReadings")

SENSOR_TYPES = ["temperature", "humidity", "co2", "motion", "gas"]

def lambda_handler(event, context):
    results = {}
    cutoff = int(time.time()) - 300  # last 5 minutes

    for sensor in SENSOR_TYPES:
        response = table.query(
            KeyConditionExpression=Key("sensor_type").eq(sensor) &
                                   Key("timestamp").gte(cutoff),
            ScanIndexForward=False,
            Limit=20
        )
        results[sensor] = response.get("Items", [])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(results, default=str)
    }