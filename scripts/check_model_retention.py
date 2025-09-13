import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_squared_error, r2_score
import os

MODEL_FILE = "model/rul_model.pkl"
LOG_FILE = "data/sensor_logs.csv"

# Load model
model = joblib.load(MODEL_FILE)

# Load recent sensor log
df = pd.read_csv(LOG_FILE)
# Ensure numeric RUL
df = df[pd.to_numeric(df["rul_hours"], errors="coerce").notnull()]
recent_df = df.tail(50)  # last 50 records

X_val = recent_df[["temperature", "vibration", "pressure", "run_hours"]].values
y_true = recent_df["rul_hours"].values

y_pred = model.predict(X_val)

mse = mean_squared_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print(f"MSE={mse:.2f}, R2={r2:.2f}")
