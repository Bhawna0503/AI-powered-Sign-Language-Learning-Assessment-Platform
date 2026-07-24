import os
import joblib


class ModelLoader:

    def __init__(self):

        self.model_version = "RandomForest_v1"

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        model_dir = os.path.join(base_dir, "models")

        self.model_path = os.path.join(
            model_dir,
            "random_forest_model.pkl"
        )

        self.encoder_path = os.path.join(
            model_dir,
            "label_encoder.pkl"
        )

        self.model = None
        self.encoder = None

    def load_model(self):

        if self.model is None:
            self.model = joblib.load(self.model_path)

        if self.encoder is None:
            self.encoder = joblib.load(self.encoder_path)

        return self.model

    def get_encoder(self):

        if self.encoder is None:
            self.encoder = joblib.load(self.encoder_path)

        return self.encoder

    def get_version(self):

        return self.model_version