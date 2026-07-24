import numpy as np


class Predictor:

    def __init__(self, model, encoder):

        self.model = model
        self.encoder = encoder

    def predict(self, feature_vector):

        X = np.array(feature_vector).reshape(1, -1)

        prediction = self.model.predict(X)[0]

        label = self.encoder.inverse_transform(
            [prediction]
        )[0]

        confidence = 1.0

        probabilities = {}

        if hasattr(self.model, "predict_proba"):

            probs = self.model.predict_proba(X)[0]

            confidence = float(max(probs))

            probabilities = {
                str(lbl): float(prob)
                for lbl, prob in zip(
                    self.encoder.classes_,
                    probs
                )
            }

        return label, confidence, probabilities