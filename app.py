import os
import time

from cpu_load_generator import load_all_cores
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def check_page():
    print("checking page")
    return "The server is running!"


@app.route("/api/latency-test", methods=["POST"])
def latency_test():
    if type(request.json) is not dict:
        print("invalid json")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    latency = request.json.get("latency", 0)
    print("starting latency test: {}s".format(latency))
    time.sleep(latency)
    print("finished latency test")
    return jsonify({"status": "success", "message": f"Responded after {latency} seconds"}), 200


@app.route("/api/request-count-test", methods=["POST"])
def request_count_test():
    if type(request.json) is not dict:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    count = request.json.get("requestCount", 0)
    response_code = request.json.get("responseCode", 200)
    print(f"Request count test: {count} requests with response code {response_code}")
    return jsonify({"status": "success", "message": "Request received"}), response_code


@app.route("/api/cpu-test", methods=["POST"])
def cpu_test():
    if type(request.json) is not dict:
        print("invalid json")
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    duration = request.json.get("duration", 0)
    load_persent = request.json.get("load", 0)
    load = int(load_persent) / 100
    print(f"Starting CPU test for {duration} seconds with {load_persent}% load")
    load_all_cores(duration_s=duration, target_load=load)
    print("finished CPU test")
    return jsonify(
        {"status": "success", "message": f"CPU test started for {duration} seconds with {load_persent}% load"}
    )


@app.route("/api/memory-test", methods=["POST"])
def memory_test():
    if type(request.json) is not dict:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    duration = request.json.get("duration", 0)
    size_Mi = request.json.get("size_Mi", 0)

    print(f"Starting memory test for {duration}s with {size_Mi} MiB")
    size_bytes = size_Mi * 1024 * 1024
    large_object = bytearray(size_bytes)
    time.sleep(duration)
    del large_object
    print("finished memory test")
    return jsonify({"status": "success", "message": f"Memory test started for {duration} seconds with {size_Mi} MiB"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
