"""
ai_engine.py

AI Recognition Engine

Workflow

Camera Frame
    ↓
Hand Detection
    ↓
Landmark Extraction
    ↓
Landmark Validation
    ↓
Normalization
    ↓
Feature Vector
    ↓
Random Forest Prediction
    ↓
Prediction Result
"""

import time
import numpy as np
import pandas as pd

from app.ai.hand_tracking.detector import HandDetector
from app.ai.hand_tracking.landmark_extractor import LandmarkExtractor
from app.ai.feature_preprocessor import FeaturePreprocessor
from app.ai.model_loader import ModelLoader
from app.ai.prediction_result import PredictionResult
from app.ai.logger import InferenceLogger


class AIEngine:
    """
    End-to-End AI Recognition Engine.
    """

    def __init__(self):

        # -----------------------------------------
        # Hand Detection
        # -----------------------------------------

        self.detector = HandDetector()

        # -----------------------------------------
        # Landmark Extraction
        # -----------------------------------------

        self.extractor = LandmarkExtractor()

        # -----------------------------------------
        # Feature Processing
        # -----------------------------------------

        self.preprocessor = FeaturePreprocessor()

        # -----------------------------------------
        # Model Loader
        # -----------------------------------------

        self.loader = ModelLoader()

        self.model = self.loader.load_model()

        # Label encoder
        self.encoder = self.loader.get_encoder()

        # -----------------------------------------
        # Inference Logger
        # -----------------------------------------

        self.logger = InferenceLogger()

        print("\n========== AI ENGINE INITIALIZED ==========")
        print("Model Version :", self.loader.get_version())

    # =========================================================
    # Prediction
    # =========================================================

    def predict(self, frame):

        start_time = time.perf_counter()

        print("\n========== AI PREDICTION STARTED ==========")

        # =====================================================
        # 1. Validate Frame
        # =====================================================

        if frame is None:

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="Invalid camera frame.",
                probabilities={},
                landmarks=[],
                hands_detected=0,
                hand_detected=False
            )

        # =====================================================
        # 2. Detect Hand
        # =====================================================

        results = self.detector.detect(frame)

        hand_detected = (
            results is not None
            and results.multi_hand_landmarks is not None
        )

        print("Hand Detected :", hand_detected)

        # -----------------------------------------
        # No Hand
        # -----------------------------------------

        if not hand_detected:

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="No hand detected.",
                probabilities={},
                landmarks=[],
                hands_detected=0,
                hand_detected=False
            )

        # =====================================================
        # 3. Count Hands
        # =====================================================

        hands_detected = len(
            results.multi_hand_landmarks
        )

        print("Hands Detected :", hands_detected)

        # =====================================================
        # 4. Reject Multiple Hands
        # =====================================================

        if hands_detected > 1:

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message=(
                    "Multiple hands detected. "
                    "Please show only one hand."
                ),
                probabilities={},
                landmarks=[],
                hands_detected=hands_detected,
                hand_detected=True
            )

        # =====================================================
        # 5. Extract Landmarks
        # =====================================================

        all_landmarks = (
            self.extractor.extract_landmarks(
                results
            )
        )

        print(
            "Landmarks Extracted :",
            len(all_landmarks)
        )

        # -----------------------------------------
        # Landmark Extraction Failed
        # -----------------------------------------

        if len(all_landmarks) == 0:

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="Landmark extraction failed.",
                probabilities={},
                landmarks=[],
                hands_detected=hands_detected,
                hand_detected=True
            )

        # First detected hand
        landmarks = all_landmarks[0]

        print(
            "Number of Landmarks :",
            len(landmarks)
        )

        # =====================================================
        # 6. Validate Landmarks
        # =====================================================

        if not self.preprocessor.validate_landmarks(
            landmarks
        ):

            return PredictionResult(
                predicted_label="",
                confidence=0.0,
                inference_time_ms=0.0,
                model_version=self.loader.get_version(),
                success=False,
                message="Invalid landmark data.",
                probabilities={},
                landmarks=landmarks,
                hands_detected=hands_detected,
                hand_detected=True
            )

        print(
            "Landmarks Validated Successfully"
        )

        # =====================================================
        # 7. Normalize Landmarks
        # =====================================================

        normalized = (
            self.preprocessor.normalize(
                landmarks
            )
        )

        print(
            "Normalization Completed"
        )

        # =====================================================
        # 8. Create Feature Vector
        # =====================================================

        features = (
            self.preprocessor.create_feature_vector(
                normalized
            )
        )

        print(
            "Feature Vector Size :",
            len(features)
        )

        # =====================================================
        # 9. Prepare Model Input
        # =====================================================

        try:

            feature_names = (
                self.model.feature_names_in_
            )

            X = pd.DataFrame(
                [features],
                columns=feature_names
            )

        except Exception:

            X = np.array(
                features
            ).reshape(1, -1)

        # =====================================================
        # 10. Model Prediction
        # =====================================================

        prediction_index = (
            self.model.predict(X)[0]
        )

        print(
            "Prediction Index :",
            prediction_index
        )

        # =====================================================
        # 11. Decode Prediction
        # =====================================================

        try:

            prediction = (
                self.encoder.inverse_transform(
                    [prediction_index]
                )[0]
            )

        except Exception:

            prediction = str(
                prediction_index
            )

        print(
            "Predicted Letter :",
            prediction
        )

        # =====================================================
        # 12. Prediction Probabilities
        # =====================================================

        confidence = 1.0

        probabilities = {}

        if hasattr(
            self.model,
            "predict_proba"
        ):

            probs = (
                self.model.predict_proba(X)[0]
            )

            classes = (
                self.model.classes_
            )

            decoded_classes = []

            for cls in classes:

                try:

                    decoded_label = (
                        self.encoder.inverse_transform(
                            [cls]
                        )[0]
                    )

                except Exception:

                    decoded_label = str(
                        cls
                    )

                decoded_classes.append(
                    decoded_label
                )

            probabilities = {

                str(label): round(
                    float(prob),
                    4
                )

                for label, prob in zip(
                    decoded_classes,
                    probs
                )
            }

            confidence = float(
                np.max(probs)
            )

        print(
            "Confidence :",
            round(
                confidence,
                4
            )
        )

        # =====================================================
        # 13. Confidence Threshold
        # =====================================================

        CONFIDENCE_THRESHOLD = 0.50

        if confidence < CONFIDENCE_THRESHOLD:

            prediction = "Unknown Gesture"

            print(
                "Prediction rejected due to "
                "low confidence."
            )

        # =====================================================
        # 14. Top Predictions
        # =====================================================

        if probabilities:

            sorted_predictions = sorted(

                probabilities.items(),

                key=lambda item: item[1],

                reverse=True
            )

            print(
                "\nTop Predictions"
            )

            for label, probability in (
                sorted_predictions[:5]
            ):

                print(
                    f"{label:5s} : "
                    f"{probability:.2%}"
                )

        # =====================================================
        # 15. Inference Time
        # =====================================================

        inference_time = (

            time.perf_counter()
            - start_time

        ) * 1000

        print(
            "Inference Time :",
            round(
                inference_time,
                2
            ),
            "ms"
        )

        # =====================================================
        # 16. Logging
        # =====================================================

        self.logger.log_prediction(

            predicted_label=str(
                prediction
            ),

            confidence=confidence,

            inference_time=inference_time,

            model_version=(
                self.loader.get_version()
            )
        )

        print(
            "Prediction Logged Successfully"
        )

        # =====================================================
        # 17. Final Prediction Result
        # =====================================================

        print(
            "\n========== AI PREDICTION COMPLETED =========="
        )

        return PredictionResult(

            predicted_label=str(
                prediction
            ),

            confidence=round(
                confidence,
                4
            ),

            inference_time_ms=round(
                inference_time,
                2
            ),

            model_version=(
                self.loader.get_version()
            ),

            success=True,

            message="Prediction Successful",

            probabilities=probabilities,

            # IMPORTANT:
            # Send the extracted landmarks forward
            # to the Feedback Engine.
            landmarks=landmarks,

            hands_detected=(
                hands_detected
            ),

            hand_detected=True
        )


# ==========================================================
# Singleton AI Engine
# ==========================================================

_engine = AIEngine()


# ==========================================================
# Public Prediction Function
# ==========================================================

def predict(frame):
    """
    Public prediction function used by GestureService.
    """

    try:

        return _engine.predict(
            frame
        )

    except Exception as e:

        print(
            "\n========== AI ENGINE ERROR =========="
        )

        print(
            str(e)
        )

        return PredictionResult(

            predicted_label="",

            confidence=0.0,

            inference_time_ms=0.0,

            model_version=(
                _engine.loader.get_version()
            ),

            success=False,

            message=str(e),

            probabilities={},

            landmarks=[],

            hands_detected=0,

            hand_detected=False
        )