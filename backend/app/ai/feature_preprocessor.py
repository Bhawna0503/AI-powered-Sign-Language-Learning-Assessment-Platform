class FeaturePreprocessor:
    """
    Performs feature validation and preprocessing.
    """

    def validate_landmarks(self, landmarks):
        """
        Validate that exactly 21 landmarks are present.
        """

        if landmarks is None:
            return False

        return len(landmarks) == 21

    def normalize(self, landmarks):
        """
        DO NOT normalize the landmarks.

        Your training dataset was created with:
            NORMALIZE = False

        So the live prediction must use the raw MediaPipe
        landmark coordinates exactly as they are.
        """

        return landmarks

    def create_feature_vector(self, landmarks):
        """
        Convert 21 landmarks into a 63-dimensional feature vector.
        """

        features = []

        for point in landmarks:
            features.extend([
                float(point["x"]),
                float(point["y"]),
                float(point["z"])
            ])

        return features