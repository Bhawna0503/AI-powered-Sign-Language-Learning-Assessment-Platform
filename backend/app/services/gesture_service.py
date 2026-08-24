from app.schemas.prediction import (
    PredictionResponse
)

from app.ai_engine.predictor import (
    Predictor
)


class GestureService:

    def __init__(self):

        self.predictor = Predictor()

    # ======================================================
    # PREDICT
    # ======================================================

    def predict(self, image):

        result = (
            self.predictor.predict(
                image
            )
        )

        # --------------------------------------------------
        # No valid prediction
        # --------------------------------------------------

        if result is None:

            return PredictionResponse(

                predicted_label="UNKNOWN",

                confidence=0.0,

                processing_time=0.0,

                expected_label="",

                correct=False,

                accuracy=0.0
            )

        # --------------------------------------------------
        # Invalid input
        # --------------------------------------------------

        if isinstance(result, dict):

            return PredictionResponse(

                predicted_label="UNKNOWN",

                confidence=0.0,

                processing_time=0.0,

                expected_label="",

                correct=False,

                accuracy=0.0
            )

        # --------------------------------------------------
        # Normal prediction
        # --------------------------------------------------

        return PredictionResponse(

            predicted_label=result.label,

            confidence=float(
                result.confidence
            ),

            processing_time=float(
                result.inference_time
            ),

            expected_label=result.expected,

            correct=bool(
                result.correct
            ),

            accuracy=float(
                result.accuracy
            )
        )