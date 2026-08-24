from app.ai_engine.predictor import Predictor


class AssessmentService:

    def __init__(self):
        self.predictor = Predictor()

    def start_practice(self, lesson_id):
        return {
            "lesson_id": lesson_id,
            "status": "Practice Started",
            "message": "Camera will open for assessment."
        }

    def open_camera(self):
        return {
            "status": "Camera Opened"
        }

    def extract_landmarks(self):
        return {
            "status": "Hand Landmarks Extracted"
        }

    def predict(self, image):
        return self.predictor.predict(image)

    def end_session(self):
        return {
            "status": "Session Ended"
        }