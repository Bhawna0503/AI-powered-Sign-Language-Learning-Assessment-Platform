from dataclasses import dataclass
from typing import Optional


@dataclass
class PredictionResult:
    """
    Standard prediction object returned by the AI engine.
    """

    predicted_label: str

    confidence: float

    inference_time_ms: float

    model_version: str

    success: bool

    message: str

    probabilities: Optional[dict] = None