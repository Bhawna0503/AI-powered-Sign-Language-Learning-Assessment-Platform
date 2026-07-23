import time
import numpy as np

from app.ai.model_loader import ModelLoader
from app.ai.feature_preprocessor import FeaturePreprocessor
from app.ai.prediction_result import PredictionResult
from app.ai.logger import InferenceLogger


class Predictor:
    """
    Production-ready AI prediction engine.
    """

    def __init__(self):

        self.loader = ModelLoader()

        self.model = self.loader.load_model()

        self.preprocessor = FeaturePreprocessor()

        self.logger = InferenceLogger()

    def predict(self, landmarks):
        """
        Parameters
        ----------
        landmarks : list
            List of 21 landmarks.
            Each landmark is:
            {
                "x": float,
                "y": float,
                "z": float
            }

        Returns
        -------
        PredictionResult
        """

        start_time = time.perf_counter()

        # ----------------------------------
        # Validate landmarks
        # ----------------------------------

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

        # ----------------------------------
        # Normalize
        # ----------------------------------

        normalized = self.preprocessor.normalize(landmarks)

        # ----------------------------------
        # Feature Vector
        # ----------------------------------

        features = self.preprocessor.create_feature_vector(normalized)

        X = np.array(features).reshape(1, -1)

        # ----------------------------------
        # Prediction
        # ----------------------------------

        prediction = self.model.predict(X)[0]

        probabilities = {}

        confidence = 1.0

        if hasattr(self.model, "predict_proba"):

            probs = self.model.predict_proba(X)[0]

            classes = self.model.classes_

            probabilities = {
                str(label): float(prob)
                for label, prob in zip(classes, probs)
            }

            confidence = float(max(probs))

        # ----------------------------------
        # Confidence Threshold
        # ----------------------------------

        if confidence < 0.60:

            prediction = "Unknown Gesture"

        end_time = time.perf_counter()

        inference_time = (end_time - start_time) * 1000

        # ----------------------------------
        # Logging
        # ----------------------------------

        self.logger.log_prediction(
            prediction,
            confidence,
            inference_time,
            self.loader.get_version()
        )

        # ----------------------------------
        # Return
        # ----------------------------------

        return PredictionResult(
            predicted_label=str(prediction),
            confidence=confidence,
            inference_time_ms=inference_time,
            model_version=self.loader.get_version(),
            success=True,
            message="Prediction Successful",
            probabilities=probabilities
        )