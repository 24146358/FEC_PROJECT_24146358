from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    print(f"  RECEIVED → sensor: {data['sensor_type']:15} | value: {data['value']} | unit: {data['unit']}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
    