import time

from datetime import datetime

from app.ai_engine.input_validator import (
    InputValidator
)

from app.ai_engine.landmark_extractor import (
    LandmarkExtractor
)

from app.ai_engine.preprocessor import (
    Preprocessor
)

from app.ai_engine.model_loader import (
    ModelLoader
)

from app.ai_engine.prediction_result import (
    PredictionResult
)

from app.ai_engine.frame_buffer import (
    FrameBuffer
)

from app.ai_engine.sequence_builder import (
    SequenceBuilder
)

from app.ai_engine.stable_prediction import (
    StablePrediction
)

from app.ai_engine.logger import logger

from app.services.practice_service import (
    PracticeService
)

from app.services.progress_service import (
    ProgressService
)

from app.services.report_service import (
    ReportService
)

from app.services.review_service import (
    ReviewService
)

from app.services.motion_metrics_service import (
    MotionMetricsService
)

from app.services.error_analysis_service import (
    ErrorAnalysisService
)

from app.services.personalized_feedback_service import (
    PersonalizedFeedbackService
)

from app.services.learner_profile_service import (
    LearnerProfileService
)

from app.services.recommendation_service import (
    RecommendationService
)

from app.services.adaptive_learning_service import (
    AdaptiveLearningService
)

from app.feedback.landmark_comparator import (
    LandmarkComparator
)

from app.feedback.rule_engine import (
    RuleEngine
)

from app.feedback.feedback_generator import (
    FeedbackGenerator
)

from app.ai.models.assessment_record import (
    AssessmentRecord
)


class Predictor:
    """
    Complete AI gesture prediction pipeline.

    Pipeline:

        Image
          ↓
        MediaPipe
          ↓
        63 raw landmarks
          ↓
        Normalization
          ↓
        Random Forest
          ↓
        Label Encoder
          ↓
        A/B/C/.../Y
          ↓
        Feedback + Progress
    """

    def __init__(self):

        # ==================================================
        # AI COMPONENTS
        # ==================================================

        self.extractor = (
            LandmarkExtractor()
        )

        self.preprocessor = (
            Preprocessor()
        )

        self.loader = (
            ModelLoader()
        )

        self.validator = (
            InputValidator()
        )

        # --------------------------------------------------
        # Load model immediately
        # --------------------------------------------------

        self.model = (
            self.loader.load_model()
        )

        # Also load encoder so startup catches
        # encoder problems early.

        self.loader.load_label_encoder()

        # ==================================================
        # APPLICATION SERVICES
        # ==================================================

        self.practice = (
            PracticeService()
        )

        self.progress = (
            ProgressService()
        )

        self.profile = (
            LearnerProfileService()
        )

        self.recommendation = (
            RecommendationService()
        )

        self.adaptive = (
            AdaptiveLearningService()
        )

        self.report = (
            ReportService(
                self.progress
            )
        )

        # ==================================================
        # FRAME / SEQUENCE
        # ==================================================

        self.frame_buffer = (
            FrameBuffer(
                max_frames=20
            )
        )

        self.sequence_builder = (
            SequenceBuilder()
        )

        # --------------------------------------------------
        # IMPORTANT:
        #
        # Keep this at 1 during initial testing.
        # --------------------------------------------------

        self.stable_prediction = (
            StablePrediction(
                required_frames=1
            )
        )

        # ==================================================
        # FEEDBACK
        # ==================================================

        self.comparator = (
            LandmarkComparator()
        )

        self.rule_engine = (
            RuleEngine()
        )

        self.feedback_generator = (
            FeedbackGenerator()
        )

        # ==================================================
        # REVIEW / ANALYSIS
        # ==================================================

        self.review = (
            ReviewService(
                self.progress
            )
        )

        self.error_analysis = (
            ErrorAnalysisService(
                self.progress
            )
        )

        self.personalized_feedback = (
            PersonalizedFeedbackService(
                self.progress,
                self.error_analysis
            )
        )

        # ==================================================
        # MOTION
        # ==================================================

        self.motion = (
            MotionMetricsService()
        )

        print(
            "\nPredictor initialized successfully."
        )

        print(
            f"Model version: "
            f"{self.loader.model_version}"
        )

    # ======================================================
    # PREDICT
    # ======================================================

    def predict(self, image):

        start_time = time.time()

        # ==================================================
        # INPUT VALIDATION
        # ==================================================

        valid, message = (
            self.validator.validate(image)
        )

        if not valid:

            logger.warning(
                "Prediction validation failed: "
                f"{message}"
            )

            return {
                "status": "invalid_input",
                "message": message
            }

        # ==================================================
        # MOTION
        # ==================================================

        self.motion.start_gesture()

        # ==================================================
        # LANDMARK EXTRACTION
        # ==================================================

        features = (
            self.extractor.extract(image)
        )

        # Debug information

        print(
            "DEBUG FEATURES:",
            (
                len(features)
                if isinstance(features, list)
                else features
            )
        )

        # ==================================================
        # HANDLE DETECTION STATES
        # ==================================================

        if features == "NO_HAND":

            logger.warning(
                "Prediction failed: "
                "no hand detected."
            )

            self.motion.add_invalid_frame()

            return None

        if features == "MULTIPLE_HANDS":

            logger.warning(
                "Prediction failed: "
                "multiple hands detected."
            )

            self.motion.add_invalid_frame()

            return None

        if features == "PARTIAL_HAND":

            logger.warning(
                "Prediction failed: "
                "partial hand detected."
            )

            self.motion.add_invalid_frame()

            return None

        if features == "NO_PERSON":

            logger.warning(
                "No person detected."
            )

            self.motion.add_invalid_frame()

            return None

        if features == "PARTIAL_BODY":

            logger.warning(
                "Partial body detected."
            )

            self.motion.add_invalid_frame()

            return None

        if features is None:

            logger.warning(
                "Landmark extraction "
                "returned None."
            )

            self.motion.add_invalid_frame()

            return None

        # ==================================================
        # VALID LANDMARKS
        # ==================================================

        self.motion.add_landmarks(
            features
        )

        # ==================================================
        # PREPROCESS
        # ==================================================

        processed = (
            self.preprocessor.preprocess(
                features
            )
        )

        # --------------------------------------------------
        # Safety check
        # --------------------------------------------------

        if processed.shape != (1, 63):

            raise ValueError(
                "Invalid processed shape: "
                f"{processed.shape}. "
                "Expected (1, 63)."
            )

        # ==================================================
        # FRAME BUFFER
        # ==================================================

        self.frame_buffer.add_frame(
            processed.flatten()
        )

        if self.frame_buffer.is_full():

            sequence = (
                self.sequence_builder.build(
                    self.frame_buffer.get_sequence()
                )
            )

            # Reserved for future temporal model.

        # ==================================================
        # RANDOM FOREST PREDICTION
        # ==================================================

        encoded_prediction = (
            self.model.predict(
                processed
            )[0]
        )

        print(
            "DEBUG ENCODED PREDICTION:",
            encoded_prediction
        )

        # ==================================================
        # DECODE NUMERICAL LABEL
        # ==================================================

        prediction = (
            self.loader.decode_label(
                encoded_prediction
            )
        )

        print(
            "DEBUG DECODED PREDICTION:",
            prediction
        )

        # ==================================================
        # STABLE PREDICTION
        # ==================================================

        stable_prediction = (
            self.stable_prediction.update(
                prediction
            )
        )

        print(
            "DEBUG STABLE PREDICTION:",
            stable_prediction
        )

        if stable_prediction is None:

            return None

        prediction = (
            stable_prediction
        )

        # ==================================================
        # CONFIDENCE
        # ==================================================

        probabilities = (
            self.model.predict_proba(
                processed
            )[0]
        )

        confidence = float(
            max(probabilities)
        )

        print(
            "DEBUG CONFIDENCE:",
            confidence
        )

        self.motion.add_confidence(
            confidence
        )

        # ==================================================
        # INFERENCE TIME
        # ==================================================

        inference_time = (
            time.time() -
            start_time
        )

        # ==================================================
        # EXPECTED LETTER
        # ==================================================

        expected = (
            self.practice.current_letter()
        )

        # ==================================================
        # CORRECTNESS
        # ==================================================

        is_correct = (
            prediction == expected
        )

        # ==================================================
        # FEEDBACK
        # ==================================================

        landmark_features = (
            self.comparator.compare(
                features
            )
        )

        rules = (
            self.rule_engine.evaluate(
                expected=expected,
                predicted=prediction,
                features=landmark_features
            )
        )

        feedback = (
            self.feedback_generator.generate(
                rules
            )
        )

        # ==================================================
        # PRACTICE
        # ==================================================

        self.practice.record_attempt(
            is_correct
        )

        if is_correct:

            self.practice.next_letter()

        # ==================================================
        # PROGRESS
        # ==================================================

        self.progress.add_attempt(

            expected=expected,

            predicted=prediction,

            correct=is_correct,

            confidence=confidence,

            inference_time=inference_time
        )

        # ==================================================
        # LEARNER PROFILE
        # ==================================================

        self.profile.update(

            expected=expected,

            correct=is_correct,

            confidence=confidence
        )

        # ==================================================
        # SESSION ACCURACY
        # ==================================================

        session_accuracy = (
            self.progress.accuracy()
        )

        # ==================================================
        # REPORT
        # ==================================================

        try:

            self.report.export_json()

        except Exception as exc:

            logger.warning(
                f"Report export failed: {exc}"
            )

        # ==================================================
        # REVIEW
        # ==================================================

        try:

            review = (
                self.review.generate_review()
            )

            print(
                "\n========== PRACTICE REVIEW =========="
            )

            print(
                f"Overall Score      : "
                f"{review.get('overall_score', 0)}%"
            )

            print(
                f"Correct Gestures   : "
                f"{review.get('correct', 0)}"
            )

            print(
                f"Incorrect Gestures : "
                f"{review.get('incorrect', 0)}"
            )

            print(
                f"Average Confidence : "
                f"{review.get('average_confidence', 0)}"
            )

            print(
                f"Strongest Gesture  : "
                f"{review.get('strongest_gesture', 'N/A')}"
            )

            print(
                f"Weakest Gesture    : "
                f"{review.get('weakest_gesture', 'N/A')}"
            )

            print(
                f"Most Common Mistake: "
                f"{review.get('most_common_mistake', 'N/A')}"
            )

            print(
                "=====================================\n"
            )

        except Exception as exc:

            logger.warning(
                f"Review generation failed: {exc}"
            )

        # ==================================================
        # MOTION METRICS
        # ==================================================

        try:

            gesture_time = (
                self.motion.gesture_time()
            )

            invalid_frames = (
                self.motion.invalid_frames
            )

            gesture_confidence = (
                self.motion.average_confidence()
            )

            gesture_stability = (
                self.motion.stability_score()
            )

            overall_score = (
                self.motion.overall_sign_score(
                    hand_shape_accuracy=
                    confidence * 100
                )
            )

        except Exception as exc:

            logger.warning(
                f"Motion metrics failed: {exc}"
            )

            gesture_time = 0.0

            invalid_frames = 0

            gesture_confidence = confidence

            gesture_stability = 0.0

            overall_score = (
                confidence * 100
            )

        # ==================================================
        # PERSONALIZED FEEDBACK
        # ==================================================

        try:

            analysis = (
                self.error_analysis.generate_analysis()
            )

            personalized = (
                self.personalized_feedback.generate()
            )

            print(
                "\n===== PERSONALIZED FEEDBACK ====="
            )

            for message in personalized:

                print(
                    "-",
                    message
                )

            print(
                "=================================\n"
            )

            print(
                "\n========== ERROR ANALYSIS =========="
            )

            print(
                analysis
            )

            print(
                "===================================="
            )

        except Exception as exc:

            logger.warning(
                f"Personalized feedback failed: {exc}"
            )

        # ==================================================
        # ASSESSMENT RECORD
        # ==================================================

        try:

            assessment = AssessmentRecord(

                expected=expected,

                predicted=prediction,

                correct=is_correct,

                confidence=confidence,

                overall_accuracy=
                session_accuracy,

                attempt_number=
                self.progress.total_attempts(),

                inference_time=
                inference_time,

                session_accuracy=
                session_accuracy,

                timestamp=datetime.now(),

                gesture_time=
                gesture_time,

                invalid_frames=
                invalid_frames,

                gesture_stability=
                gesture_stability,

                overall_score=
                overall_score
            )

            print(
                "\nAssessment Record:"
            )

            print(
                assessment
            )

        except Exception as exc:

            logger.warning(
                f"Assessment record failed: {exc}"
            )

        # ==================================================
        # LEARNER PROFILE
        # ==================================================

        try:

            profile = (
                self.profile.profile()
            )

            print(
                "\n===== LEARNER PROFILE ====="
            )

            print(
                profile
            )

            print(
                "===========================\n"
            )

        except Exception as exc:

            logger.warning(
                f"Learner profile failed: {exc}"
            )

            profile = {}

        # ==================================================
        # RECOMMENDATIONS
        # ==================================================

        try:

            recommendations = (
                self.recommendation.recommend(
                    profile
                )
            )

            print(
                "\n===== RECOMMENDATIONS ====="
            )

            for item in recommendations:

                print(
                    f"{item['alphabet']} : "
                    f"{item['reason']}"
                )

            print(
                "===========================\n"
            )

        except Exception as exc:

            logger.warning(
                f"Recommendation generation failed: {exc}"
            )

        # ==================================================
        # ADAPTIVE PLAN
        # ==================================================

        try:

            plan = (
                self.adaptive.generate_plan(
                    profile
                )
            )

            print(
                "\n===== ADAPTIVE LEARNING PLAN ====="
            )

            print(
                "Practice Now :",
                plan.get(
                    "practice_now",
                    []
                )
            )

            print(
                "Review Later :",
                plan.get(
                    "review_later",
                    []
                )
            )

            print(
                "Mastered     :",
                plan.get(
                    "mastered",
                    []
                )
            )

            print(
                "==================================\n"
            )

        except Exception as exc:

            logger.warning(
                f"Adaptive learning plan failed: {exc}"
            )

        # ==================================================
        # SESSION DASHBOARD
        # ==================================================

        print(
            "\n========== SESSION DASHBOARD =========="
        )

        print(
            f"Expected Letter    : {expected}"
        )

        print(
            f"Predicted Letter   : {prediction}"
        )

        print(
            f"Correct            : {is_correct}"
        )

        print(
            f"Confidence         : "
            f"{confidence * 100:.2f}%"
        )

        print(
            f"Session Accuracy   : "
            f"{session_accuracy:.2f}%"
        )

        print(
            f"Inference Time     : "
            f"{inference_time:.4f} sec"
        )

        print(
            f"Gesture Time       : "
            f"{gesture_time:.2f} sec"
        )

        print(
            f"Invalid Frames     : "
            f"{invalid_frames}"
        )

        print(
            f"Gesture Stability  : "
            f"{gesture_stability:.2f}"
        )

        print(
            f"Overall Sign Score : "
            f"{overall_score:.2f}"
        )

        print(
            "========================================\n"
        )

        # ==================================================
        # RETURN API RESULT
        # ==================================================

        return PredictionResult(

            label=prediction,

            confidence=confidence,

            model_version=(
                self.loader.model_version
            ),

            inference_time=inference_time,

            feedback=feedback,

            expected=expected,

            correct=is_correct,

            accuracy=session_accuracy
        )