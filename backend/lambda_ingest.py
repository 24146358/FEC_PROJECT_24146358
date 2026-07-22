import json
import boto3
import time

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("FEC_SensorReadings")

# IoT ingest Lambda — receives fog node batches and writes to Dynamodb tables
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except Exception:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid JSON"})}

    written = 0
    for sensor_type, data in body.items():
        item = {
            "sensor_type": sensor_type,
            "timestamp": int(data.get("latest_ts", time.time())),
            "average": str(data.get("average", "")),
            "latest": str(data.get("latest", "")),
            "count": data.get("count", 0),
            "raw_readings": json.dumps(data.get("readings", []))
        }
        table.put_item(Item=item)
        written += 1

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"written": written})
    }