from pydantic import BaseModel


class PredictionResponse(BaseModel):

    predicted_label: str

    confidence: float

    processing_time: float

    expected_label: str

    correct: bool

    accuracy: float