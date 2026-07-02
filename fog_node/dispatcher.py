import requests
import os

# Replace with your actual API Gateway URL after Phase 3
CLOUD_ENDPOINT = os.getenv("CLOUD_ENDPOINT", "https://ru87w8ier8.execute-api.us-east-1.amazonaws.com/prod/ingest")

def dispatch(batch):
    if not batch:
        return
    try:
        resp = requests.post(CLOUD_ENDPOINT, json=batch, timeout=10)
        print(f"[Dispatcher] Cloud response: {resp.status_code}")
    except Exception as e:
        print(f"[Dispatcher] Failed to reach cloud: {e}")