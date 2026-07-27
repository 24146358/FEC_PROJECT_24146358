#Central configuration file for the sensor simulation
FOG_URL = "http://99.81.123.186:5000/ingest"#Fog node URL for sensor data ingestion
DATASET_PATH = "../data/iot_telemetry_data.csv"
DEFAULT_INTERVAL = 2  #seconds between readings
BATCH_DEVICE_ID = "b8:27:eb:bf:9d:51"  #single device from dataset