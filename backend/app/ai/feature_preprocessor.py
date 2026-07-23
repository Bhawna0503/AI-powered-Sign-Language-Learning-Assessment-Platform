class FeaturePreprocessor:
    """
    Performs feature validation and normalization.
    """

    def validate_landmarks(self, landmarks):
        """
        Checks whether exactly 21 landmarks are present.
        """

        if landmarks is None:
            return False

        if len(landmarks) != 21:
            return False

        return True

    def normalize(self, landmarks):
        """
        Wrist-relative normalization.
        Landmark 0 (wrist) becomes the origin.
        """

        wrist = landmarks[0]

        normalized = []

        for point in landmarks:

            normalized.append({
                "x": point["x"] - wrist["x"],
                "y": point["y"] - wrist["y"],
                "z": point["z"] - wrist["z"]
            })

        return normalized

    def create_feature_vector(self, landmarks):
        """
        Converts normalized landmarks into
        a 63-dimensional feature vector.
        """

        features = []

        for point in landmarks:

            features.extend([
                point["x"],
                point["y"],
                point["z"]
            ])

        return features