"""
report_generator.py

Generates assessment reports from practice attempts.

Features:
- Overall assessment score
- Correct / incorrect attempts
- Average confidence
- Average inference time
- Gesture-wise performance
- Most difficult gestures
- Strongest gestures
- Improvement / accuracy trend
- Confidence trend
- Predicted-vs-expected analysis
- JSON report saving
"""

import json
import os
from collections import defaultdict
from datetime import datetime


class ReportGenerator:
    """
    Generates reports and analytics from assessment attempts.
    """

    def __init__(self):

        # -----------------------------------------
        # Report Output Folder
        # -----------------------------------------

        self.output_folder = os.path.join(
            os.getcwd(),
            "reports"
        )

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    # =========================================
    # Generate Report
    # =========================================

    def generate(self, attempts):

        """
        Generate complete assessment report.

        Parameters
        ----------
        attempts : list
            List of attempt dictionaries.

        Returns
        -------
        dict
            Complete assessment report.
        """

        # -----------------------------------------
        # Empty Session
        # -----------------------------------------

        if attempts is None:
            attempts = []

        total_attempts = len(attempts)

        # -----------------------------------------
        # Correct / Incorrect
        # -----------------------------------------

        correct_attempts = sum(
            1
            for attempt in attempts
            if attempt.get("correct", False)
        )

        incorrect_attempts = (
            total_attempts - correct_attempts
        )

        # -----------------------------------------
        # Overall Score
        # -----------------------------------------

        if total_attempts > 0:

            overall_score = round(
                (
                    correct_attempts /
                    total_attempts
                ) * 100,
                2
            )

        else:

            overall_score = 0.0

        # -----------------------------------------
        # Average Confidence
        # -----------------------------------------

        if total_attempts > 0:

            average_confidence = round(

                sum(
                    float(
                        attempt.get(
                            "confidence",
                            0
                        )
                    )
                    for attempt in attempts
                )
                / total_attempts,

                3
            )

        else:

            average_confidence = 0.0

        # -----------------------------------------
        # Average Confidence Percentage
        # -----------------------------------------

        average_confidence_percentage = round(
            average_confidence * 100,
            2
        )

        # -----------------------------------------
        # Average Gesture Accuracy
        # -----------------------------------------

        if total_attempts > 0:

            average_gesture_accuracy = round(

                sum(
                    float(
                        attempt.get(
                            "gesture_accuracy",
                            attempt.get(
                                "confidence",
                                0
                            ) * 100
                        )
                    )
                    for attempt in attempts
                )
                / total_attempts,

                2
            )

        else:

            average_gesture_accuracy = 0.0

        # -----------------------------------------
        # Average Response Time
        # -----------------------------------------

        if total_attempts > 0:

            average_response_time = round(

                sum(
                    float(
                        attempt.get(
                            "inference_time_ms",
                            0
                        )
                    )
                    for attempt in attempts
                )
                / total_attempts,

                2
            )

        else:

            average_response_time = 0.0

        # -----------------------------------------
        # Gesture Statistics
        # -----------------------------------------

        gesture_stats = defaultdict(
            lambda: {
                "attempts": 0,
                "correct": 0,
                "incorrect": 0,
                "confidence_total": 0.0
            }
        )

        for attempt in attempts:

            expected = attempt.get(
                "expected_letter",
                "Unknown"
            )

            correct = attempt.get(
                "correct",
                False
            )

            confidence = float(
                attempt.get(
                    "confidence",
                    0
                )
            )

            gesture_stats[expected]["attempts"] += 1

            gesture_stats[expected]["confidence_total"] += confidence

            if correct:

                gesture_stats[expected]["correct"] += 1

            else:

                gesture_stats[expected]["incorrect"] += 1

        # -----------------------------------------
        # Gesture Performance
        # -----------------------------------------

        gesture_performance = {}

        for letter, stats in gesture_stats.items():

            attempts_count = stats["attempts"]

            if attempts_count > 0:

                accuracy = round(
                    (
                        stats["correct"] /
                        attempts_count
                    ) * 100,
                    2
                )

                avg_confidence = round(
                    stats["confidence_total"] /
                    attempts_count,
                    3
                )

            else:

                accuracy = 0.0
                avg_confidence = 0.0

            gesture_performance[letter] = {

                "attempts": attempts_count,

                "correct": stats["correct"],

                "incorrect": stats["incorrect"],

                "accuracy": accuracy,

                "average_confidence":
                    avg_confidence,

                "average_confidence_percentage":
                    round(
                        avg_confidence * 100,
                        2
                    )
            }

        # -----------------------------------------
        # Most Difficult Gestures
        # -----------------------------------------

        difficult = sorted(

            gesture_performance.items(),

            key=lambda item:
                (
                    item[1]["accuracy"],
                    -item[1]["attempts"]
                )

        )

        # -----------------------------------------
        # Strongest Gestures
        # -----------------------------------------

        strongest = sorted(

            gesture_performance.items(),

            key=lambda item:
                (
                    -item[1]["accuracy"],
                    -item[1]["attempts"]
                )

        )

        # -----------------------------------------
        # Improvement Trend
        # -----------------------------------------

        improvement = []

        for index, attempt in enumerate(
            attempts,
            start=1
        ):

            session_accuracy = attempt.get(
                "session_accuracy",
                0
            )

            improvement.append({

                "attempt": attempt.get(
                    "attempt_number",
                    index
                ),

                "session_accuracy":
                    round(
                        float(
                            session_accuracy
                        ),
                        2
                    )
            })

        # -----------------------------------------
        # Confidence Trend
        # -----------------------------------------

        confidence_trend = []

        for index, attempt in enumerate(
            attempts,
            start=1
        ):

            confidence = float(
                attempt.get(
                    "confidence",
                    0
                )
            )

            confidence_trend.append({

                "attempt": attempt.get(
                    "attempt_number",
                    index
                ),

                "confidence":
                    round(
                        confidence,
                        3
                    ),

                "confidence_percentage":
                    round(
                        confidence * 100,
                        2
                    )
            })

        # -----------------------------------------
        # Prediction Analysis
        # -----------------------------------------

        prediction_analysis = []

        for index, attempt in enumerate(
            attempts,
            start=1
        ):

            prediction_analysis.append({

                "attempt": attempt.get(
                    "attempt_number",
                    index
                ),

                "expected":
                    attempt.get(
                        "expected_letter",
                        ""
                    ),

                "predicted":
                    attempt.get(
                        "predicted_letter",
                        ""
                    ),

                "correct":
                    attempt.get(
                        "correct",
                        False
                    ),

                "confidence":
                    round(
                        float(
                            attempt.get(
                                "confidence",
                                0
                            )
                        ),
                        3
                    ),

                "inference_time_ms":
                    round(
                        float(
                            attempt.get(
                                "inference_time_ms",
                                0
                            )
                        ),
                        2
                    ),

                "timestamp":
                    attempt.get(
                        "timestamp",
                        ""
                    )
            })

        # -----------------------------------------
        # Common Mistakes
        # -----------------------------------------

        mistakes = defaultdict(int)

        for attempt in attempts:

            if not attempt.get(
                "correct",
                False
            ):

                expected = attempt.get(
                    "expected_letter",
                    "Unknown"
                )

                predicted = attempt.get(
                    "predicted_letter",
                    "Unknown"
                )

                mistake = (
                    f"{expected} -> {predicted}"
                )

                mistakes[mistake] += 1

        most_common_mistakes = sorted(

            mistakes.items(),

            key=lambda item:
                item[1],

            reverse=True
        )

        # -----------------------------------------
        # Session Status
        # -----------------------------------------

        if total_attempts == 0:

            session_status = "No attempts recorded."

        elif overall_score >= 90:

            session_status = (
                "Excellent performance."
            )

        elif overall_score >= 75:

            session_status = (
                "Good performance. "
                "Keep practicing."
            )

        elif overall_score >= 50:

            session_status = (
                "Average performance. "
                "More practice is recommended."
            )

        else:

            session_status = (
                "Needs improvement. "
                "Continue practicing the difficult gestures."
            )

        # -----------------------------------------
        # Recommended Gestures
        # -----------------------------------------

        recommended_next_gestures = [

            gesture[0]

            for gesture in difficult[:3]

        ]

        # -----------------------------------------
        # Generate Final Report
        # -----------------------------------------

        report = {

            # -----------------------------
            # Basic Information
            # -----------------------------

            "report_generated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "session_status":
                session_status,

            # -----------------------------
            # Overall Statistics
            # -----------------------------

            "total_attempts":
                total_attempts,

            "correct_attempts":
                correct_attempts,

            "incorrect_attempts":
                incorrect_attempts,

            "overall_assessment_score":
                overall_score,

            # -----------------------------
            # Confidence
            # -----------------------------

            "average_confidence":
                average_confidence,

            "average_confidence_percentage":
                average_confidence_percentage,

            "average_gesture_accuracy":
                average_gesture_accuracy,

            # -----------------------------
            # Performance
            # -----------------------------

            "average_response_time_ms":
                average_response_time,

            # -----------------------------
            # Gesture Analysis
            # -----------------------------

            "gesture_wise_performance":
                gesture_performance,

            "most_difficult_gestures":
                difficult,

            "strongest_gestures":
                strongest,

            # -----------------------------
            # Mistakes
            # -----------------------------

            "most_common_mistakes":
                [
                    {
                        "mistake": mistake,
                        "count": count
                    }

                    for mistake, count
                    in most_common_mistakes
                ],

            # -----------------------------
            # Recommendations
            # -----------------------------

            "recommended_next_gestures":
                recommended_next_gestures,

            # -----------------------------
            # Trends
            # -----------------------------

            "improvement":
                improvement,

            "confidence_trend":
                confidence_trend,

            # -----------------------------
            # Prediction Details
            # -----------------------------

            "prediction_analysis":
                prediction_analysis
        }

        return report

    # =========================================
    # Save JSON Report
    # =========================================

    def save_json(self, report):

        """
        Save report as JSON file.

        Returns
        -------
        str
            Absolute path of saved report.
        """

        path = os.path.join(
            self.output_folder,
            "assessment_report.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        return path

    # =========================================
    # Generate And Save
    # =========================================

    def generate_and_save(self, attempts):

        """
        Generate report and immediately save it.
        """

        report = self.generate(
            attempts
        )

        report_path = self.save_json(
            report
        )

        report["report_file"] = report_path

        return report

    # =========================================
    # Get Report Path
    # =========================================

    def get_report_path(self):

        return os.path.join(
            self.output_folder,
            "assessment_report.json"
        )