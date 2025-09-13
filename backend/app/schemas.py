from pydantic import BaseModel
from typing import List

class SensorData(BaseModel):
    machine_id: int          # <-- added machine_id
    temperature: float
    vibration: float
    pressure: float
    run_hours: int

class BatchSensorData(BaseModel):
    machines: List[SensorData]

class PredictionResult(BaseModel):
    machine_id: int
    rul_hours: float
    predicted_failure_date: str

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResult]
