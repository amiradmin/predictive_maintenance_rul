import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import shutil
import time

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
LOG_FILE = os.path.join(PROJECT_ROOT, "data", "sensor_logs.csv")
MODEL_FILE = os.path.join(PROJECT_ROOT, "model", "rul_model.pkl")

# Load sensor log safely
try:
    df = pd.read_csv(LOG_FILE, on_bad_lines="skip")
except FileNotFoundError:
    print("❌ No sensor log found. Cannot retrain model.")
    exit()
except pd.errors.EmptyDataError:
    print("❌ Sensor log is empty. Cannot retrain model.")
    exit()

if df.empty:
    print("❌ Sensor log is empty. Cannot retrain model.")
    exit()

# Ensure necessary columns exist
required_cols = ["temperature", "vibration", "pressure", "run_hours", "rul_hours"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"❌ Missing columns in {LOG_FILE}: {missing_cols}")
    exit()

# Convert rul_hours to numeric (drop bad rows)
before_rows = len(df)
df["rul_hours"] = pd.to_numeric(df["rul_hours"], errors="coerce")
df = df.dropna(subset=["rul_hours"])
after_rows = len(df)

if after_rows < before_rows:
    print(f"⚠️ Dropped {before_rows - after_rows} rows due to invalid rul_hours values")

if df.empty:
    print("❌ No valid data left after cleaning. Cannot retrain model.")
    exit()

# Backup old model if it exists
if os.path.exists(MODEL_FILE):
    backup_file = MODEL_FILE.replace(".pkl", f"_backup_{int(time.time())}.pkl")
    shutil.copy(MODEL_FILE, backup_file)
    print(f"📦 Backup of previous model saved to {backup_file}")

# Features and target
X = df[["temperature", "vibration", "pressure", "run_hours"]]
y = df["rul_hours"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train regression model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"✅ Retraining completed: MSE={mse:.2f}, R2={r2:.2f}")

# Save updated model
joblib.dump(model, MODEL_FILE)
print(f"💾 Updated RUL model saved to {MODEL_FILE}")
