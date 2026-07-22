# Central config — change FOG_URL to your EC2 public IP once deployed
FOG_URL = "http://54.156.77.3:5000/ingest"  # change to EC2 IP later
DATASET_PATH = "../data/iot_telemetry_data.csv"
DEFAULT_INTERVAL = 2  # seconds between readings — configurable at runtime
BATCH_DEVICE_ID = "b8:27:eb:bf:9d:51"  # use one device from dataset