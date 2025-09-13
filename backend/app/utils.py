import pandas as pd
import os
from datetime import datetime

# Absolute project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

LOG_FILE = os.path.join(PROJECT_ROOT, "data", "sensor_logs.csv")

def log_sensor_data(machine_id: int, sensor_data, rul_hours: float, predicted_date: datetime):
    """Append sensor data and predictions to CSV log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = {
        "timestamp": timestamp,
        "machine_id": machine_id,
        "temperature": sensor_data.temperature,
        "vibration": sensor_data.vibration,
        "pressure": sensor_data.pressure,
        "run_hours": sensor_data.run_hours,
        "rul_hours": rul_hours,
        "predicted_failure_date": predicted_date.strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.DataFrame([row])
    if os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)
