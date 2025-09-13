from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import BatchSensorData, BatchPredictionResponse, PredictionResult
from .model import predict_rul, predict_failure_date
from .utils import log_sensor_data, LOG_FILE
import numpy as np

app = FastAPI(title="Predictive Maintenance RUL API")

# --- Enable CORS ---
origins = [
    "http://localhost",
    "http://localhost:3000",  # React dev server
    "*",  # یا هر آدرس دیگری که نیاز دارید
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict_batch", response_model=BatchPredictionResponse)
def predict_batch(data: BatchSensorData):
    if not data.machines:
        raise HTTPException(status_code=400, detail="No machine data provided")

    # Prepare feature array safely
    X = []
    for m in data.machines:
        try:
            row = [m.temperature, m.vibration, m.pressure, m.run_hours]
            if any(v is None for v in row):
                raise ValueError
            X.append(row)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid data for machine {m.machine_id}")

    X_array = np.array(X)
    if X_array.ndim == 1:
        X_array = X_array.reshape(1, -1)

    # Predict RUL
    rul_predictions = predict_rul(X_array)

    results = []
    for i, machine in enumerate(data.machines):
        predicted_date = predict_failure_date(rul_predictions[i])
        log_sensor_data(machine.machine_id, machine, rul_predictions[i], predicted_date)
        results.append(PredictionResult(
            machine_id=machine.machine_id,
            rul_hours=float(rul_predictions[i]),
            predicted_failure_date=predicted_date.strftime("%Y-%m-%d %H:%M:%S")
        ))

    return BatchPredictionResponse(predictions=results)
