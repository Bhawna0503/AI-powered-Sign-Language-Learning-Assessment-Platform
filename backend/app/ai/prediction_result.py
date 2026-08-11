from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class PredictionResult:
    """
    Standard prediction object returned by the AI engine.

    This object stores the complete result of one AI prediction,
    including prediction, confidence, timing, hand detection,
    landmarks, probabilities, and status information.
    """

    # =========================================================
    # BASIC PREDICTION INFORMATION
    # =========================================================

    predicted_label: str

    confidence: float

    inference_time_ms: float

    model_version: str

    # =========================================================
    # STATUS
    # =========================================================

    success: bool

    message: str

    # =========================================================
    # CLASS PROBABILITIES
    # =========================================================

    probabilities: Optional[Dict[str, float]] = None

    # =========================================================
    # HAND DETECTION
    # =========================================================

    # Used by the current AI engine
    hand_detected: bool = False

    # Number of detected hands
    hands_detected: int = 0

    # =========================================================
    # LANDMARKS
    # =========================================================

    landmarks: Optional[List[Any]] = None

    # =========================================================
    # OPTIONAL METADATA
    # =========================================================

    metadata: Dict[str, Any] = field(default_factory=dict)