import pandas as pd
import itertools
import requests
import time
import argparse
import random
from config import FOG_URL, DATASET_PATH, DEFAULT_INTERVAL, BATCH_DEVICE_ID

class BaseSensor:
    def __init__(self, sensor_type, column, unit):
        self.sensor_type = sensor_type
        self.column = column
        self.unit = unit
        self.data = self._load_data()

    def _load_data(self):
        df = pd.read_csv(DATASET_PATH)
        df = df[df['device'] == BATCH_DEVICE_ID].reset_index(drop=True)
        return list(df[self.column])

    def _jitter(self, value):
        """Add tiny noise on each loop so repeated passes look realistic."""
        if isinstance(value, bool) or isinstance(value, int):
            return value
        return round(value + random.uniform(-0.01 * abs(value), 0.01 * abs(value)), 4)

    def run(self, interval=DEFAULT_INTERVAL):
        print(f"[{self.sensor_type}] Starting — interval: {interval}s")
        for raw_value in itertools.cycle(self.data):
            value = self._jitter(raw_value)
            payload = {
                "sensor_type": self.sensor_type,
                "value": value,
                "unit": self.unit,
                "timestamp": time.time()
            }
            try:
                requests.post(FOG_URL, json=payload, timeout=5)
                print(f"[{self.sensor_type}] Sent: {value} {self.unit}")
            except Exception as e:
                print(f"[{self.sensor_type}] Error: {e}")
            time.sleep(interval)