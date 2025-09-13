import os
import joblib
import numpy as np
from datetime import datetime, timedelta

# Absolute project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Paths
MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "rul_model.pkl")

# Load model
rul_model = joblib.load(MODEL_PATH)

def predict_rul(sensor_array: np.ndarray):
    """Predict RUL in hours."""
    return rul_model.predict(sensor_array)

def predict_failure_date(rul_hours: float):
    """Convert RUL to predicted failure datetime."""
    return datetime.now() + timedelta(hours=rul_hours)
