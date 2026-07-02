import time
from collections import defaultdict

BUFFER_SECONDS = 10

class Aggregator:
    def __init__(self):
        self.buffers = defaultdict(list)
        self.last_flush = time.time()

    # Validation ranges per sensor type
    VALID_RANGES = {
        "Temperature": (-20, 100),
        "Humidity":    (0, 100),
        "CO":         (0, 10),
        "Smoke":         (0, 1),
        "Motion":      (0, 1),
    }

    def is_valid(self, sensor_type, value):
        if sensor_type not in self.VALID_RANGES:
            return True
        lo, hi = self.VALID_RANGES[sensor_type]
        try:
            return lo <= float(value) <= hi
        except (TypeError, ValueError):
            return False

    def add(self, sensor_type, value, timestamp):
        if not self.is_valid(sensor_type, value):
            print(f"[Aggregator] Discarded invalid {sensor_type}: {value}")
            return
        self.buffers[sensor_type].append({
            "value": value,
            "timestamp": timestamp
        })

    def should_flush(self):
        return (time.time() - self.last_flush) >= BUFFER_SECONDS

    def flush(self):
        """Return aggregated batch and clear buffers."""
        batch = {}
        for sensor_type, readings in self.buffers.items():
            if not readings:
                continue
            numeric = []
            for r in readings:
                try:
                    numeric.append(float(r["value"]))
                except (TypeError, ValueError):
                    pass
            batch[sensor_type] = {
                "count": len(readings),
                "average": round(sum(numeric) / len(numeric), 4) if numeric else None,
                "latest": readings[-1]["value"],
                "latest_ts": readings[-1]["timestamp"],
                "readings": readings[-5:]  # keep last 5 raw readings
            }
        self.buffers.clear()
        self.last_flush = time.time()
        return batch