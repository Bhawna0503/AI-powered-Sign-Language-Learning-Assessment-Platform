from collections import deque


class StablePrediction:
    """
    Stabilizes predictions over multiple frames.

    For now the application can use required_frames=1
    so that every valid frame immediately produces
    a prediction.

    Later this can be changed to 3 or 5 for webcam
    stability.
    """

    def __init__(self, required_frames=1):

        self.required_frames = (
            required_frames
        )

        self.predictions = deque(
            maxlen=required_frames
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update(self, prediction):

        if prediction is None:

            return None

        self.predictions.append(
            prediction
        )

        # --------------------------------------------------
        # Not enough predictions yet
        # --------------------------------------------------

        if (
            len(self.predictions)
            < self.required_frames
        ):

            return None

        # --------------------------------------------------
        # required_frames = 1
        # --------------------------------------------------

        if self.required_frames == 1:

            return prediction

        # --------------------------------------------------
        # Majority voting
        # --------------------------------------------------

        counts = {}

        for item in self.predictions:

            counts[item] = (
                counts.get(item, 0) + 1
            )

        stable_prediction = max(
            counts,
            key=counts.get
        )

        return stable_prediction

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.predictions.clear()