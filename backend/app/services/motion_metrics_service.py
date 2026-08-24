import time
import numpy as np

class MotionMetricsService:

    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = None
        self.invalid_frames = 0
        self.confidences = []
        self.landmark_history=[]

    def start_gesture(self):
        if self.start_time is None:
            self.start_time = time.time()

    def add_invalid_frame(self):
        self.invalid_frames += 1

    def add_confidence(self, confidence):
        self.confidences.append(confidence)

    def gesture_time(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def average_confidence(self):
        if not self.confidences:
            return 0
        return sum(self.confidences) / len(self.confidences)

    def add_landmarks(self, landmarks):
        self.landmark_history.append(landmarks)

    def stability_score(self):
        if len(self.landmark_history) < 2:
            return 100.0

        data = np.array(self.landmark_history)
        movement = np.std(data, axis=0).mean()

        score = max(0, 100 - movement * 1000)
        return round(score, 2)
    def overall_sign_score(self, hand_shape_accuracy):
        confidence = self.average_confidence() * 100
        stability = self.stability_score()

        time_taken = self.gesture_time()

        if time_taken <= 2:
            timing_score = 100
        elif time_taken <= 4:
            timing_score = 80
        elif time_taken <= 6:
            timing_score = 60
        else:
            timing_score = 40

        score = (
            hand_shape_accuracy * 0.5 +
            confidence * 0.2 +
            stability * 0.2 +
            timing_score * 0.1
        )

        return round(score, 2)