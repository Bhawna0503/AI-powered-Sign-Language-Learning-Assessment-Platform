from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssessmentRecord:
    expected: str
    predicted: str
    correct: bool
    confidence: float
    overall_accuracy: float
    attempt_number: int
    inference_time: float
    session_accuracy: float
    timestamp: datetime
    gesture_time: float
    invalid_frames: int
    gesture_stability: float
    overall_score: float