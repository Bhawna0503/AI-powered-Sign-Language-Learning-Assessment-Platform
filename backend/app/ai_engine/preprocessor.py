import numpy as np

from app.ai.ml.preprocessing.normalize_landmarks import (
    normalize_sample
)


class Preprocessor:
    """
    Preprocesses raw MediaPipe landmarks before
    sending them to the Random Forest.

    Input:
        63 raw landmark values

    Output:
        1 × 63 normalized feature array
    """

    @staticmethod
    def preprocess(features):

        if features is None:

            raise ValueError(
                "Features cannot be None."
            )

        # --------------------------------------------------
        # Convert to NumPy array
        # --------------------------------------------------

        features = np.asarray(
            features,
            dtype=np.float64
        )

        # --------------------------------------------------
        # Validate feature count
        # --------------------------------------------------

        if features.size != 63:

            raise ValueError(
                f"Expected 63 features, "
                f"got {features.size}."
            )

        # --------------------------------------------------
        # SAME normalization used during training
        # --------------------------------------------------

        normalized = normalize_sample(
            features
        )

        normalized = np.asarray(
            normalized,
            dtype=np.float64
        )

        # --------------------------------------------------
        # Random Forest expects:
        #
        # (1, 63)
        # --------------------------------------------------

        return normalized.reshape(
            1,
            63
        )