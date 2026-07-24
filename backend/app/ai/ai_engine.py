import time
import numpy as np

from app.ai.hand_tracking.detector import HandDetector
from app.ai.hand_tracking.landmark_extractor import LandmarkExtractor
from app.ai.feature_preprocessor import FeaturePreprocessor
from app.ai.model_loader import ModelLoader
from app.ai.prediction_result import PredictionResult
from app.ai.logger import InferenceLogger


class AIEngine:
    """
    End-to-End AI Recognition Engine

    Pipeline:
        Image/Webcam Frame
                │
                ▼
        MediaPipe Hand Detection
                │
                ▼
        Landmark Extraction
                │
                ▼
        Landmark Validation
                │
                ▼
        Feature Normalization
                │
                ▼
        Feature Vector Generation
                │
                ▼
        Model Loading
                │
                ▼
        Prediction
                │
                ▼
        Confidence Calculation
                │
                ▼
        Structured Prediction Result
    """

    def __init__(self):

        self.detector = HandDetector()

        self.extractor = LandmarkExtractor()

        self.preprocessor = FeaturePreprocessor()

        self.loader = ModelLoader()

        self.model = self.loader.load_model()

        self.logger = InferenceLogger()

    def predict(self, frame):
        """
        Predict gesture from a webcam/image frame.

        Parameters
        ----------
        frame : numpy.ndarray

        Returns
        -------
        PredictionResult
        """

        start_time = time.perf_counter()

        # =====================================
        # Detect Hand
        # =====================================

        results = self.detector.detect(frame)

        if not results.multi_hand_landmarks:

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="No hand detected.",
                probabilities={}
            )

        # =====================================
        # Reject Multiple Hands
        # =====================================

        if len(results.multi_hand_landmarks) > 1:

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="Multiple hands detected.",
                probabilities={}
            )

        # =====================================
        # Extract Landmarks
        # =====================================

        landmarks = self.extractor.extract_landmarks(results)

        if len(landmarks) == 0:

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="Landmark extraction failed.",
                probabilities={}
            )

        landmarks = landmarks[0]

        # =====================================
        # Validate Landmarks
        # =====================================

        if not self.preprocessor.validate_landmarks(landmarks):

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="Invalid landmark data.",
                probabilities={}
            )

        # =====================================
        # Normalize Landmarks
        # =====================================

        normalized_landmarks = self.preprocessor.normalize(landmarks)

        # =====================================
        # Create Feature Vector
        # =====================================

        feature_vector = self.preprocessor.create_feature_vector(
            normalized_landmarks
        )

        X = np.array(feature_vector).reshape(1, -1)

        # =====================================
        # Predict Gesture
        # =====================================

        prediction = self.model.predict(X)[0]

        confidence = 1.0

        probabilities = {}

        if hasattr(self.model, "predict_proba"):

            probs = self.model.predict_proba(X)[0]

            classes = self.model.classes_

            probabilities = {
                str(label): float(prob)
                for label, prob in zip(classes, probs)
            }

            confidence = float(max(probs))

        # =====================================
        # Confidence Threshold
        # =====================================

        if confidence < 0.60:

            prediction = "Unknown Gesture"

        # =====================================
        # Measure Inference Time
        # =====================================

        end_time = time.perf_counter()

        inference_time = (end_time - start_time) * 1000

        # =====================================
        # Log Prediction
        # =====================================

        self.logger.log_prediction(
            predicted_label=str(prediction),
            confidence=confidence,
            inference_time=inference_time,
            model_version=self.loader.get_version()
        )

        # =====================================
        # Return Structured Result
        # =====================================

        return PredictionResult(
            predicted_label=str(prediction),
            confidence=confidence,
            inference_time_ms=inference_time,
            model_version=self.loader.get_version(),
            success=True,
            message="Prediction Successful",
            probabilities=probabilities
        )


# =====================================================
# Singleton AI Engine
# =====================================================

_engine = AIEngine()


# =====================================================
# Public Function
# =====================================================

def predict(frame):
    """
    Public interface for gesture prediction.

    Usage:

        from app.ai.ai_engine import predict

        result = predict(frame)
    """

    return _engine.predict(frame)