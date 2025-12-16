import json
import time
import random
import threading
import requests
from datetime import datetime

with open("config.json") as f:
    config = json.load(f)

ENDPOINT = config["endpoint_url"]

def generate_value(sensor_type):
    if sensor_type == "temperature":
        return round(random.uniform(18, 30), 2)
    elif sensor_type == "humidity":
        return round(random.uniform(40, 75), 2)
    elif sensor_type == "light":
        return random.randint(100, 1000)
    return None

def sensor_worker(sensor):
    while True:
        payload = {
            "sensor_type": sensor["type"],
            "value": generate_value(sensor["type"]),
            "location": sensor["location"],
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            r = requests.post(ENDPOINT, json=payload, timeout=1)
            print(f"[{sensor['type']}] {r.status_code} -> {payload}")
        except Exception as e:
            print(f"[ERROR] {sensor['type']} -> {e}")

        time.sleep(sensor["frequency_ms"] / 1000)

threads = []
for sensor in config["sensors"]:
    t = threading.Thread(target=sensor_worker, args=(sensor,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
