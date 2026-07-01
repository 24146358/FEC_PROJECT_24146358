from flask import Flask, request, jsonify
import threading
import time
from aggregator import Aggregator
from dispatcher import dispatch

app = Flask(__name__)
aggregator = Aggregator()

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    aggregator.add(
        data.get("sensor_type"),
        data.get("value"),
        data.get("timestamp")
    )
    return jsonify({"status": "received"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "fog node running"}), 200

def flush_loop():
    """Background thread: flush and dispatch every BUFFER_SECONDS."""
    while True:
        time.sleep(1)
        if aggregator.should_flush():
            batch = aggregator.flush()
            if batch:
                print(f"[FogNode] Dispatching batch: {list(batch.keys())}")
                dispatch(batch)

if __name__ == "__main__":
    t = threading.Thread(target=flush_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)