import cv2
import mediapipe as mp


class LandmarkExtractor:
    """
    Extracts 21 hand landmarks from an input image.

    MediaPipe produces:

        21 landmarks × 3 values
        = 63 raw features

    IMPORTANT:

    The Random Forest model is trained using
    normalized landmarks.

    Therefore this class ONLY extracts raw
    MediaPipe landmarks.

    Normalization is handled by Preprocessor.
    """

    def __init__(self):

        self.mp_hands = (
            mp.solutions.hands
        )

        self.hands = (
            self.mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=2,
                min_detection_confidence=0.5
            )
        )

    # ======================================================
    # EXTRACT LANDMARKS
    # ======================================================

    def extract(self, image):
        """
        Extract 63 raw MediaPipe landmark values.

        Returns:

            list of 63 values

        OR:

            NO_HAND
            MULTIPLE_HANDS
            None
        """

        if image is None:

            return None

        # --------------------------------------------------
        # Convert BGR -> RGB
        # --------------------------------------------------

        try:

            rgb_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

        except Exception:

            return None

        # --------------------------------------------------
        # MediaPipe detection
        # --------------------------------------------------

        results = self.hands.process(
            rgb_image
        )

        # --------------------------------------------------
        # No hand
        # --------------------------------------------------

        if not results.multi_hand_landmarks:

            return "NO_HAND"

        # --------------------------------------------------
        # Multiple hands
        # --------------------------------------------------

        if (
            len(results.multi_hand_landmarks)
            > 1
        ):

            return "MULTIPLE_HANDS"

        # --------------------------------------------------
        # Single hand
        # --------------------------------------------------

        hand_landmarks = (
            results.multi_hand_landmarks[0]
        )

        # --------------------------------------------------
        # Extract x, y, z
        # --------------------------------------------------

        features = []

        for landmark in (
            hand_landmarks.landmark
        ):

            features.extend(
                [
                    float(landmark.x),
                    float(landmark.y),
                    float(landmark.z)
                ]
            )

        # --------------------------------------------------
        # Safety check
        # --------------------------------------------------

        if len(features) != 63:

            return None

        return features