import json
import boto3
from boto3.dynamodb.conditions import Key
import time

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("FEC_SensorReadings")

SENSOR_TYPES = ["Temperature", "Humidity", "CO", "Motion", "Smoke"]

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "content-type",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
            },
            "body": ""
        }

    results = {}
    cutoff = int(time.time()) - 300

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
            "Access-Control-Allow-Headers": "content-type",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Content-Type": "application/json"
        },
        "body": json.dumps(results, default=str)
    }