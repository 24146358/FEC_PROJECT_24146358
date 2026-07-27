Smart Building IoT Pipeline — Fog and Edge Computing (H9FECC)
Student: Oluwapelumi | NCI MSc Cloud Computing

ARCHITECTURE
  Sensor simulators (Python) → Flask fog node (EC2) → API Gateway → Lambda → DynamoDB → S3 Dashboard

PREREQUISITES
  - Python 3.10+
  - pip install pandas flask requests
  - AWS account with EC2, Lambda, DynamoDB, API Gateway, S3

RUNNING SENSORS LOCALLY
  cd sensors
  python run_sensors.py
  (or individually: python temperature_sensor.py --interval 2)

RUNNING THE FOG NODE
  cd fog_node
  export CLOUD_ENDPOINT="https://YOUR_API_GW/prod/ingest"
  python app.py

DATASET
  Kaggle: Environmental Sensor Telemetry Data (garystafford)
  Place iot_telemetry_data.csv in /data/

DASHBOARD
  Hosted on S3 static website — URL in project report

GITHUB ACTIONS CI/CD
  Any push to main automatically redeploys Lambda functions