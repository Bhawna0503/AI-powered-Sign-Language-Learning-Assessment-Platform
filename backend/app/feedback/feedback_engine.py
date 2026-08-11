"""
feedback_engine.py

Central feedback generation module.

Workflow:

Expected Gesture
        ↓
Predicted Gesture
        ↓
Landmark Comparison
        ↓
Rule Evaluation
        ↓
Human-readable Feedback

The landmark comparison is used only when the prediction
is incorrect or when additional gesture-quality analysis
is explicitly required.
"""

from app.feedback.landmark_comparator import LandmarkComparator
from app.feedback.rule_engine import RuleEngine


class FeedbackEngine:

    def __init__(self):

        self.comparator = LandmarkComparator()
        self.rule_engine = RuleEngine()

    # =====================================================
    # MAIN FEEDBACK FUNCTION
    # =====================================================

    def generate_feedback(
        self,
        expected_letter,
        predicted_letter,
        confidence,
        landmarks=None
    ):

        confidence_percentage = round(
            confidence * 100,
            2
        )

        # =================================================
        # CASE 1: CORRECT PREDICTION
        # =================================================
        #
        # If the AI predicted the expected gesture,
        # don't generate correction messages.
        #
        # This prevents messages such as:
        #
        # "Straighten your index finger"
        #
        # when the user actually performed the
        # correct gesture.
        # =================================================

        if expected_letter == predicted_letter:

            return {
                "status": "Correct",

                "message":
                    "Excellent! You performed the sign correctly.",

                "expected":
                    expected_letter,

                "predicted":
                    predicted_letter,

                "confidence":
                    confidence_percentage,

                "corrections":
                    []
            }

        # =================================================
        # CASE 2: INCORRECT PREDICTION
        # =================================================

        comparison = {}

        corrections = []

        # -------------------------------------------------
        # Run landmark comparison only for incorrect
        # predictions.
        # -------------------------------------------------

        if landmarks is not None:

            try:

                comparison = self.comparator.compare(
                    landmarks
                )

                corrections = self.rule_engine.evaluate(
                    comparison
                )

            except Exception as e:

                print(
                    "Feedback landmark comparison warning:",
                    str(e)
                )

                comparison = {}

                corrections = []

        # =================================================
        # CONFIDENCE-BASED MESSAGE
        # =================================================

        if confidence >= 0.90:

            message = (
                f"You showed '{predicted_letter}' "
                f"instead of '{expected_letter}'. "
                "Your hand shape is clear, but it represents "
                "another sign."
            )

        elif confidence >= 0.70:

            message = (
                f"Your gesture is close to "
                f"'{expected_letter}'. "
                "Try adjusting your finger positions."
            )

        else:

            message = (
                "Low confidence detected. "
                "Keep your entire hand inside the camera "
                "frame and perform the gesture again."
            )

        # =================================================
        # FINAL INCORRECT FEEDBACK
        # =================================================

        return {

            "status":
                "Incorrect",

            "message":
                message,

            "expected":
                expected_letter,

            "predicted":
                predicted_letter,

            "confidence":
                confidence_percentage,

            "corrections":
                corrections
        }