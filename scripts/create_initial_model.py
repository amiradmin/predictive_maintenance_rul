# scripts/create_initial_model.py
import joblib
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import os

MODEL_FILE = os.path.join(os.path.dirname(__file__), "../model/rul_model.pkl")

# Create a dummy dataset
X_dummy = np.random.rand(100, 4) * 100  # 100 samples, 4 features
y_dummy = np.random.rand(100) * 500      # RUL in hours

# Train a simple RandomForestRegressor
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_dummy, y_dummy)

# Save model
os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
joblib.dump(model, MODEL_FILE)
print(f"Initial RUL model saved to {MODEL_FILE}")
