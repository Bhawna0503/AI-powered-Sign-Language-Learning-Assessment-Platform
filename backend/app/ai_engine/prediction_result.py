from dataclasses import dataclass


@dataclass
class PredictionResult:
    """
    Result returned by the AI prediction pipeline.
    """

    label: str

    confidence: float

    model_version: str

    inference_time: float

    feedback: dict

    expected: str

    correct: bool

    accuracy: float