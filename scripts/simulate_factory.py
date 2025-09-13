import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime
import os

NUM_MACHINES = 5
LOG_FILE = os.path.join(os.path.dirname(__file__), "../data/sensor_logs.csv")
API_URL = "http://127.0.0.1:8000/predict_batch"

# Define the expected columns
COLUMNS = [
    "machine_id", "temperature", "vibration", "pressure", "run_hours",
    "rul_hours", "predicted_failure_date", "timestamp"
]

def simulate_sensor_data(machine_id):
    """Generate simulated sensor readings"""
    temperature = np.random.normal(70, 10)
    vibration = np.random.normal(0.5, 0.1)
    pressure = np.random.normal(30, 5)
    run_hours = np.random.randint(100, 2000)
    return {
        "machine_id": machine_id,
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
        "run_hours": run_hours
    }

def main():
    while True:
        machines_data = [simulate_sensor_data(i+1) for i in range(NUM_MACHINES)]

        # Send data to API
        payload = {"machines": machines_data}
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                predictions = response.json()["predictions"]
                for p in predictions:
                    for m in machines_data:
                        if m["machine_id"] == p["machine_id"]:
                            m["rul_hours"] = p["rul_hours"]
                            m["predicted_failure_date"] = p["predicted_failure_date"]
                print(f"✅ Sent data to API: {predictions}")
            else:
                print(f"❌ API error: {response.status_code} - {response.text}")
        except:
            print("⚠️ API not running, using dummy RUL values")
            for m in machines_data:
                m["rul_hours"] = np.random.randint(50, 500)
                m["predicted_failure_date"] = (
                    datetime.now() + pd.to_timedelta(m["rul_hours"], unit="h")
                ).strftime("%Y-%m-%d %H:%M:%S")

        # Add timestamp
        for m in machines_data:
            m["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to CSV with consistent columns
        df = pd.DataFrame(machines_data, columns=COLUMNS)
        if os.path.exists(LOG_FILE):
            df.to_csv(LOG_FILE, mode="a", header=False, index=False)
        else:
            df.to_csv(LOG_FILE, index=False)

        print(f"📝 Logged data for {NUM_MACHINES} machines at {datetime.now()}")
        time.sleep(5)

if __name__ == "__main__":
    main()
