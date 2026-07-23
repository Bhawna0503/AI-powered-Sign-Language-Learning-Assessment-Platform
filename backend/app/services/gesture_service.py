import time


class GestureService:

    def __init__(self):
        pass

    def open_camera(self):

        return {
            "status": "Camera Opened"
        }

    def extract_landmarks(self):

        return {
            "status": "21 Hand Landmarks Extracted"
        }

    def predict(self):

        start = time.time()

        prediction = "A"
        confidence = 0.98

        processing_time = time.time() - start

        return {
            "prediction": prediction,
            "confidence": confidence,
            "processing_time": processing_time
        }

    def finish_session(self):

        return {
            "status": "Practice Session Finished"
        }