import os
import joblib


class ModelLoader:
    """
    Loads the trained ML model and stores version information.
    """

    def __init__(self):

        self.model_version = "RandomForest_v1"

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        self.model_path = os.path.join(
            base_dir,
            "models",
            "random_forest_model.pkl"
        )

        self.model = None

    def load_model(self):

        if self.model is None:

            if not os.path.exists(self.model_path):

                raise FileNotFoundError(
                    f"Model not found:\n{self.model_path}"
                )

            self.model = joblib.load(self.model_path)

        return self.model

    def get_version(self):

        return self.model_version