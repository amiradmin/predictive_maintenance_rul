from fastapi import FastAPI
from .schemas import BatchSensorData, BatchPredictionResponse, PredictionResult
from .model import predict_rul, predict_failure_date
from .utils import log_sensor_data, LOG_FILE
import numpy as np

app = FastAPI(title="Predictive Maintenance RUL API")


@app.post("/predict_batch", response_model=BatchPredictionResponse)
def predict_batch(data: BatchSensorData):
    # Prepare feature array
    X = np.array([[m.temperature, m.vibration, m.pressure, m.run_hours] for m in data.machines])

    # Predict RUL for all machines
    rul_predictions = predict_rul(X)

    results = []
    for i, machine in enumerate(data.machines):
        predicted_date = predict_failure_date(rul_predictions[i])

        # Use the machine_id from input instead of i+1
        log_sensor_data(machine.machine_id, machine, rul_predictions[i], predicted_date)

        results.append(PredictionResult(
            machine_id=machine.machine_id,
            rul_hours=float(rul_predictions[i]),
            predicted_failure_date=predicted_date.strftime("%Y-%m-%d %H:%M:%S")
        ))

    return BatchPredictionResponse(predictions=results)
