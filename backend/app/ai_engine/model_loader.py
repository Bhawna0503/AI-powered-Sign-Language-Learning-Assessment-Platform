from pathlib import Path

import joblib


class ModelLoader:
    """
    Loads the trained Random Forest model and label encoder.

    Model:
        63 normalized MediaPipe landmark features
        24 ASL alphabet classes.

    Random Forest predicts encoded labels:
        0, 1, 2, ..., 23

    LabelEncoder converts them to:
        A, B, C, ..., Y
    """

    def __init__(self):

        self.model = None

        self.label_encoder = None

        self.model_version = (
            "RF-63F-24CLASS-v2.0"
        )

        # --------------------------------------------------
        # PROJECT ROOT
        # --------------------------------------------------
        #
        # app/ai_engine/model_loader.py
        #
        # parents[0] = ai_engine
        # parents[1] = app
        # parents[2] = backend
        #

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        # --------------------------------------------------
        # MODEL DIRECTORY
        # --------------------------------------------------

        self.models_dir = (
            self.project_root / "models"
        )

        # --------------------------------------------------
        # MODEL FILES
        # --------------------------------------------------

        self.model_path = (
            self.models_dir /
            "random_forest_model.pkl"
        )

        self.encoder_path = (
            self.models_dir /
            "label_encoder.pkl"
        )

    # ======================================================
    # LOAD RANDOM FOREST
    # ======================================================

    def load_model(self):

        if self.model is not None:

            return self.model

        if not self.model_path.exists():

            raise FileNotFoundError(
                "Random Forest model not found:\n"
                f"{self.model_path}"
            )

        print(
            "\nLoading Random Forest model..."
        )

        self.model = joblib.load(
            self.model_path
        )

        # --------------------------------------------------
        # Validate feature count
        # --------------------------------------------------

        expected_features = getattr(
            self.model,
            "n_features_in_",
            None
        )

        if expected_features != 63:

            raise ValueError(
                "Incorrect Random Forest model.\n"
                f"Expected 63 features, "
                f"but model expects "
                f"{expected_features}."
            )

        # --------------------------------------------------
        # Validate number of classes
        # --------------------------------------------------

        number_of_classes = len(
            self.model.classes_
        )

        if number_of_classes != 24:

            raise ValueError(
                "Incorrect number of model classes.\n"
                f"Expected 24, "
                f"found {number_of_classes}."
            )

        print(
            "Random Forest loaded successfully."
        )

        print(
            f"Model path : {self.model_path}"
        )

        print(
            f"Features   : {expected_features}"
        )

        print(
            f"Trees      : {self.model.n_estimators}"
        )

        print(
            f"Classes    : {number_of_classes}"
        )

        return self.model

    # ======================================================
    # LOAD LABEL ENCODER
    # ======================================================

    def load_label_encoder(self):

        if self.label_encoder is not None:

            return self.label_encoder

        if not self.encoder_path.exists():

            raise FileNotFoundError(
                "Label encoder not found:\n"
                f"{self.encoder_path}"
            )

        print(
            "\nLoading label encoder..."
        )

        self.label_encoder = joblib.load(
            self.encoder_path
        )

        # --------------------------------------------------
        # Validate encoder
        # --------------------------------------------------

        classes = list(
            self.label_encoder.classes_
        )

        if len(classes) != 24:

            raise ValueError(
                "Incorrect label encoder.\n"
                f"Expected 24 classes, "
                f"found {len(classes)}."
            )

        print(
            "Label encoder loaded successfully."
        )

        print(
            "Classes:",
            classes
        )

        return self.label_encoder

    # ======================================================
    # DECODE MODEL PREDICTION
    # ======================================================

    def decode_label(self, encoded_label):
        """
        Convert Random Forest numerical prediction
        into the actual alphabet label.

        Example:

            0 -> A
            1 -> B
            2 -> C
        """

        encoder = (
            self.load_label_encoder()
        )

        try:

            encoded_label = int(
                encoded_label
            )

            label = (
                encoder.inverse_transform(
                    [encoded_label]
                )[0]
            )

        except Exception as exc:

            raise ValueError(
                f"Could not decode model "
                f"prediction: {encoded_label}"
            ) from exc

        return str(label)

    # ======================================================
    # GET SUPPORTED CLASSES
    # ======================================================

    def get_classes(self):

        encoder = (
            self.load_label_encoder()
        )

        return [
            str(label)
            for label in encoder.classes_
        ]