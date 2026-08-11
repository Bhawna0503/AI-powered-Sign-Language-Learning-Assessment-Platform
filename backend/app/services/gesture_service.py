"""
gesture_service.py

Connects the AI engine with the assessment system.

Browser workflow:

React Browser Camera
        ↓
Image/JPEG
        ↓
FastAPI
        ↓
GestureService.predict_frame()
        ↓
AI Engine
        ↓
MediaPipe
        ↓
21 Landmarks
        ↓
Random Forest
        ↓
AssessmentService
        ↓
Feedback Engine
        ↓
JSON Response
"""

from app.ai.ai_engine import predict as ai_predict
from app.learning.assessment_service import AssessmentService
from app.feedback.feedback_engine import FeedbackEngine


class GestureService:

    def __init__(self):

        self.frame = None

        self.feedback = FeedbackEngine()

        self.assessment = AssessmentService()

        print("GestureService initialized.")

    # ========================================================
    # START PRACTICE
    # ========================================================

    def start_practice(self):

        print("\n========== PRACTICE STARTED ==========")

        return self.assessment.start_practice()

    # ========================================================
    # CURRENT LETTER
    # ========================================================

    def get_current_letter(self):

        letter = self.assessment.get_current_letter()

        print("Current Letter :", letter)

        return letter

    # ========================================================
    # PREDICT FRAME
    # ========================================================

    def predict_frame(self, frame):

        print("\n========== AI FRAME PREDICTION ==========")

        if frame is None:

            raise ValueError(
                "No image frame received."
            )

        self.frame = frame

        # ----------------------------------------------------
        # Run AI prediction
        # ----------------------------------------------------

        result = ai_predict(frame)

        print("Predicted Letter :", result.predicted_label)
        print("Confidence       :", result.confidence)
        print("Inference Time   :", result.inference_time_ms)
        print("Model Version    :", result.model_version)
        print("Success          :", result.success)
        print("Message          :", result.message)

        return result

    # ========================================================
    # PROCESS AI RESULT
    # ========================================================

    def process_prediction_result(self, result):

        print(
            "\n========== PROCESSING ASSESSMENT =========="
        )

        if result is None:

            raise ValueError(
                "Prediction result is missing."
            )

        # ----------------------------------------------------
        # AI prediction failed
        # ----------------------------------------------------

        if not result.success:

            return {
                "success": False,
                "message": result.message,
                "predicted_letter": result.predicted_label,
                "confidence": result.confidence,
                "inference_time_ms": result.inference_time_ms,
                "model_version": result.model_version
            }

        # ----------------------------------------------------
        # Get landmarks
        # ----------------------------------------------------

        landmarks = getattr(
            result,
            "landmarks",
            None
        )

        # ----------------------------------------------------
        # Send prediction to AssessmentService
        # ----------------------------------------------------

        assessment_result = self.assessment.process_prediction(

            predicted_letter=result.predicted_label,

            confidence=result.confidence,

            inference_time_ms=result.inference_time_ms,

            landmarks=landmarks
        )

        print(
            "\n========== ASSESSMENT COMPLETED =========="
        )

        print(assessment_result)

        return assessment_result

    # ========================================================
    # COMPLETE FRAME → PREDICTION → ASSESSMENT
    # ========================================================

    def predict_and_assess(self, frame):

        """
        Complete browser prediction workflow.

        frame
          ↓
        AI prediction
          ↓
        Assessment
          ↓
        Feedback
        """

        result = self.predict_frame(frame)

        return self.process_prediction_result(result)

    # ========================================================
    # OLD COMPATIBILITY METHOD
    # ========================================================

    def predict(self):

        """
        Compatibility method for older API code.

        Uses self.frame if available.
        """

        if self.frame is None:

            raise ValueError(
                "No frame available for prediction."
            )

        return self.predict_and_assess(
            self.frame
        )

    # ========================================================
    # NEXT LETTER
    # ========================================================

    def next_letter(self):

        letter = self.assessment.next_letter()

        print(
            "Next Letter :",
            letter
        )

        return letter

    # ========================================================
    # PREVIOUS LETTER
    # ========================================================

    def previous_letter(self):

        if hasattr(
            self.assessment,
            "previous_letter"
        ):

            return self.assessment.previous_letter()

        return None

    # ========================================================
    # SELECT LETTER
    # ========================================================

    def select_letter(self, letter):

        if hasattr(
            self.assessment,
            "select_letter"
        ):

            return self.assessment.select_letter(
                letter
            )

        return None

    # ========================================================
    # SESSION STATISTICS
    # ========================================================

    def get_statistics(self):

        print(
            "\n========== SESSION STATISTICS =========="
        )

        stats = self.assessment.get_session_statistics()

        print(stats)

        return stats

    # ========================================================
    # ATTEMPT HISTORY
    # ========================================================

    def get_history(self):

        print(
            "\n========== ATTEMPT HISTORY =========="
        )

        history = self.assessment.get_attempt_history()

        print(history)

        return history

    # ========================================================
    # LAST ATTEMPT
    # ========================================================

    def get_last_attempt(self):

        history = self.assessment.get_attempt_history()

        if not history:

            return None

        return history[-1]

    # ========================================================
    # ASSESSMENT REPORT
    # ========================================================

    def generate_report(self):

        print(
            "\n========== ASSESSMENT REPORT =========="
        )

        report = self.assessment.generate_report()

        print(report)

        return report

    # ========================================================
    # PRACTICE REVIEW
    # ========================================================

    def generate_review(self):

        print(
            "\n========== PRACTICE REVIEW =========="
        )

        review = self.assessment.generate_review()

        print(review)

        return review

    # ========================================================
    # END SESSION
    # ========================================================

    def end_session(self):

        print(
            "\n========== END SESSION =========="
        )

        self.frame = None

        # SessionManager is inside AssessmentService.
        # End it directly if available.

        try:

            self.assessment.session.end_session()

        except Exception as e:

            print(
                "Session end warning:",
                str(e)
            )

        print(
            "Session ended successfully."
        )

        return {
            "success": True,
            "message": "Practice session ended."
        }

    # ========================================================
    # FINISH SESSION
    # ========================================================

    def finish_session(self):

        """
        Compatibility method.

        Browser owns the camera, so there is no
        cv2.VideoCapture object to release here.
        """

        print(
            "\n========== FINISH SESSION =========="
        )

        self.frame = None

        try:

            return self.end_session()

        except Exception as e:

            print(
                "Finish session warning:",
                str(e)
            )

            return {
                "success": True,
                "message": "Session finished."
            }