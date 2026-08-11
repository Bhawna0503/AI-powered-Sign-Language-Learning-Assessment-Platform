"""
assessment_service.py

Coordinates the complete learning and assessment workflow.
"""

from app.learning.lesson_manager import LessonManager
from app.learning.session_manager import SessionManager
from app.learning.attempt_tracker import AttemptTracker
from app.learning.report_generator import ReportGenerator
from app.feedback.feedback_engine import FeedbackEngine


class AssessmentService:
    """
    Controls the complete learning session.
    """

    def __init__(self):

        self.lesson = LessonManager()
        self.session = SessionManager()
        self.tracker = AttemptTracker()
        self.report = ReportGenerator()

        # Feedback Engine
        self.feedback_engine = FeedbackEngine()

    # =========================================
    # Start Practice
    # =========================================

    def start_practice(self):

        print("\n========== ASSESSMENT SESSION START ==========")

        self.lesson.start_practice()
        self.session.reset()
        self.tracker.clear()

        print("Assessment session initialized.")

        return {
            "status": "started",
            "current_letter": self.lesson.get_current_letter()
        }

    # =========================================
    # Current Letter
    # =========================================

    def get_current_letter(self):

        return self.lesson.get_current_letter()

    # =========================================
    # Process Prediction
    # =========================================

    def process_prediction(
        self,
        predicted_letter: str,
        confidence: float,
        inference_time_ms: float,
        landmarks=None,
    ):

        # -----------------------------------------
        # Get Expected Letter
        # -----------------------------------------

        expected = self.lesson.get_current_letter()

        # -----------------------------------------
        # Clean Prediction
        # -----------------------------------------

        if predicted_letter is None:
            predicted_letter = ""

        predicted_letter = str(
            predicted_letter
        ).strip()

        expected = str(
            expected
        ).strip()

        # -----------------------------------------
        # Validate Confidence
        # -----------------------------------------

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.0

        confidence = max(
            0.0,
            min(1.0, confidence)
        )

        # -----------------------------------------
        # Validate Inference Time
        # -----------------------------------------

        try:
            inference_time_ms = float(
                inference_time_ms
            )
        except (TypeError, ValueError):
            inference_time_ms = 0.0

        # -----------------------------------------
        # Check Correctness
        # -----------------------------------------

        correct = (
            expected.upper() ==
            predicted_letter.upper()
        )

        # -----------------------------------------
        # Update Session
        # -----------------------------------------

        self.session.record_attempt(
            correct
        )

        session_accuracy = (
            self.session.get_accuracy()
        )

        # -----------------------------------------
        # Gesture Accuracy
        # -----------------------------------------

        gesture_accuracy = round(
            confidence * 100,
            2
        )

        # -----------------------------------------
        # Generate Feedback
        # -----------------------------------------

        feedback = (
            self.feedback_engine.generate_feedback(
                expected_letter=expected,
                predicted_letter=predicted_letter,
                confidence=confidence,
                landmarks=landmarks,
            )
        )

        # -----------------------------------------
        # Store Attempt
        # -----------------------------------------

        self.tracker.add_attempt(

            expected_letter=expected,

            predicted_letter=predicted_letter,

            confidence=confidence,

            inference_time_ms=inference_time_ms,

            session_accuracy=session_accuracy
        )

        # -----------------------------------------
        # Build Result
        # -----------------------------------------

        result = {

            "attempt_number":
                self.tracker.total_attempts(),

            "expected_letter":
                expected,

            "predicted_letter":
                predicted_letter,

            "correct":
                correct,

            "confidence":
                round(
                    confidence,
                    3
                ),

            "gesture_accuracy":
                gesture_accuracy,

            "inference_time_ms":
                round(
                    inference_time_ms,
                    2
                ),

            "session_accuracy":
                round(
                    session_accuracy,
                    2
                ),

            "feedback":
                feedback
        }

        print("\n========== ASSESSMENT RESULT ==========")
        print(result)

        return result

    # =========================================
    # Next Letter
    # =========================================

    def next_letter(self):

        return self.lesson.next_letter()

    # =========================================
    # Previous Letter
    # =========================================

    def previous_letter(self):

        return self.lesson.previous_letter()

    # =========================================
    # Select Letter
    # =========================================

    def select_letter(
        self,
        letter: str
    ):

        return self.lesson.select_letter(
            letter
        )

    # =========================================
    # Restart Practice
    # =========================================

    def restart(self):

        self.lesson.restart()
        self.session.reset()
        self.tracker.clear()

        return {
            "status": "restarted",
            "current_letter":
                self.lesson.get_current_letter()
        }

    # =========================================
    # Lesson Status
    # =========================================

    def get_lesson_status(self):

        return self.lesson.get_status()

    # =========================================
    # Session Statistics
    # =========================================

    def get_session_statistics(self):

        return {

            "total_attempts":
                self.tracker.total_attempts(),

            "correct_attempts":
                self.tracker.correct_attempts(),

            "incorrect_attempts":
                self.tracker.incorrect_attempts(),

            "session_accuracy":
                round(
                    self.session.get_accuracy(),
                    2
                ),

            "average_confidence":
                self.tracker.average_confidence(),

            "average_gesture_accuracy":
                self.tracker.average_gesture_accuracy(),

            "average_response_time":
                self.tracker.average_response_time(),

            "current_letter":
                self.lesson.get_current_letter()
        }

    # =========================================
    # Attempt History
    # =========================================

    def get_attempt_history(self):

        return self.tracker.get_attempts()

    # =========================================
    # Last Attempt
    # =========================================

    def get_last_attempt(self):

        return self.tracker.get_last_attempt()

    # =========================================
    # Assessment Report
    # =========================================

    def generate_report(self):

        attempts = (
            self.tracker.get_attempts()
        )

        report = self.report.generate(
            attempts
        )

        report_path = (
            self.report.save_json(
                report
            )
        )

        report["report_file"] = (
            report_path
        )

        return report

    # =========================================
    # Practice Review
    # =========================================

    def generate_review(self):

        attempts = (
            self.tracker.get_attempts()
        )

        report = self.report.generate(
            attempts
        )

        # -----------------------------------------
        # Confidence Trend
        # -----------------------------------------

        confidence_trend = [

            {
                "attempt":
                    attempt.get(
                        "attempt_number",
                        index + 1
                    ),

                "confidence":
                    attempt.get(
                        "confidence",
                        0
                    ),

                "confidence_percentage":
                    round(
                        attempt.get(
                            "confidence",
                            0
                        ) * 100,
                        2
                    )
            }

            for index, attempt
            in enumerate(attempts)
        ]

        # -----------------------------------------
        # Gesture Feedback
        # -----------------------------------------

        gesture_feedback = []

        for attempt in attempts:

            feedback = (
                self.feedback_engine.generate_feedback(

                    expected_letter=
                        attempt.get(
                            "expected_letter",
                            ""
                        ),

                    predicted_letter=
                        attempt.get(
                            "predicted_letter",
                            ""
                        ),

                    confidence=
                        attempt.get(
                            "confidence",
                            0
                        ),

                    # Landmark data is not currently
                    # stored inside AttemptTracker.
                    landmarks=None
                )
            )

            gesture_feedback.append({

                "attempt":
                    attempt.get(
                        "attempt_number"
                    ),

                "expected":
                    attempt.get(
                        "expected_letter"
                    ),

                "predicted":
                    attempt.get(
                        "predicted_letter"
                    ),

                "correct":
                    attempt.get(
                        "correct"
                    ),

                "feedback":
                    feedback
            })

        # -----------------------------------------
        # Difficult Gestures
        # -----------------------------------------

        difficult = report.get(
            "most_difficult_gestures",
            []
        )

        # -----------------------------------------
        # Recommended Gestures
        # -----------------------------------------

        recommended = [

            gesture[0]

            for gesture in difficult[:3]

            if isinstance(
                gesture,
                (list, tuple)
            )
            and len(gesture) > 0
        ]

        # -----------------------------------------
        # Final Review
        # -----------------------------------------

        review = {

            "overall_score":
                report.get(
                    "overall_assessment_score",
                    0
                ),

            "total_attempts":
                report.get(
                    "total_attempts",
                    0
                ),

            "correct_attempts":
                report.get(
                    "correct_attempts",
                    0
                ),

            "incorrect_attempts":
                report.get(
                    "incorrect_attempts",
                    0
                ),

            "average_confidence":
                report.get(
                    "average_confidence",
                    0
                ),

            "session_status":
                report.get(
                    "session_status",
                    ""
                ),

            "confidence_trend":
                confidence_trend,

            "most_common_mistakes":
                report.get(
                    "most_common_mistakes",
                    []
                ),

            "most_difficult_gestures":
                difficult,

            "gesture_feedback":
                gesture_feedback,

            "recommended_next_gestures":
                recommended
        }

        return review

    # =========================================
    # End Session
    # =========================================

    def end_session(self):

        self.session.end_session()

        return {
            "status": "completed",
            "statistics":
                self.get_session_statistics()
        }