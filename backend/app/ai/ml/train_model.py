import joblib
import pandas as pd

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.preprocessing import LabelEncoder


class GestureModelTrainer:

    def __init__(self):

        # app/ai/ml/train_model.py
        # parents[0] = ml
        # parents[1] = ai
        # parents[2] = app
        # parents[3] = backend

        current_file = Path(__file__).resolve()

        self.project_root = current_file.parents[3]

        self.output_dir = self.project_root / "output"

        self.model_dir = self.project_root / "models"

        self.model_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        # --------------------------------------------------
        # Dataset paths
        # --------------------------------------------------

        self.train_path = (
            self.output_dir / "train.csv"
        )

        self.validation_path = (
            self.output_dir / "validation.csv"
        )

        self.test_path = (
            self.output_dir / "test.csv"
        )

        # --------------------------------------------------
        # Model paths
        # --------------------------------------------------

        self.model_path = (
            self.model_dir /
            "random_forest_model.pkl"
        )

        self.encoder_path = (
            self.model_dir /
            "label_encoder.pkl"
        )

    # ======================================================
    # LOAD DATA
    # ======================================================

    def load_data(self):

        print("=" * 60)
        print("LOADING DATA")
        print("=" * 60)

        for path in [
            self.train_path,
            self.validation_path,
            self.test_path
        ]:

            if not path.exists():

                raise FileNotFoundError(
                    f"Dataset file not found:\n{path}"
                )

        train_df = pd.read_csv(
            self.train_path
        )

        validation_df = pd.read_csv(
            self.validation_path
        )

        test_df = pd.read_csv(
            self.test_path
        )

        X_train = train_df.iloc[:, :-1]
        y_train = train_df.iloc[:, -1]

        X_validation = validation_df.iloc[:, :-1]
        y_validation = validation_df.iloc[:, -1]

        X_test = test_df.iloc[:, :-1]
        y_test = test_df.iloc[:, -1]

        # --------------------------------------------------
        # Validate feature count
        # --------------------------------------------------

        for name, X in [
            ("Training", X_train),
            ("Validation", X_validation),
            ("Test", X_test)
        ]:

            if X.shape[1] != 63:

                raise ValueError(
                    f"{name} dataset contains "
                    f"{X.shape[1]} features. "
                    f"Expected 63."
                )

        print(
            f"Training samples   : {len(X_train)}"
        )

        print(
            f"Validation samples : {len(X_validation)}"
        )

        print(
            f"Test samples       : {len(X_test)}"
        )

        print(
            f"Features           : {X_train.shape[1]}"
        )

        print(
            f"Classes            : {y_train.nunique()}"
        )

        return (
            X_train,
            y_train,
            X_validation,
            y_validation,
            X_test,
            y_test
        )

    # ======================================================
    # TRAIN
    # ======================================================

    def train(self):

        (
            X_train,
            y_train,
            X_validation,
            y_validation,
            X_test,
            y_test
        ) = self.load_data()

        # --------------------------------------------------
        # Encode labels
        # --------------------------------------------------

        print()
        print("=" * 60)
        print("ENCODING LABELS")
        print("=" * 60)

        encoder = LabelEncoder()

        y_train_encoded = encoder.fit_transform(
            y_train
        )

        y_validation_encoded = encoder.transform(
            y_validation
        )

        y_test_encoded = encoder.transform(
            y_test
        )

        print(
            "Classes:",
            list(encoder.classes_)
        )

        # --------------------------------------------------
        # Train Random Forest
        # --------------------------------------------------

        print()
        print("=" * 60)
        print("TRAINING RANDOM FOREST")
        print("=" * 60)

        model = RandomForestClassifier(

            n_estimators=300,

            max_features="sqrt",

            min_samples_leaf=1,

            random_state=42,

            n_jobs=-1
        )

        model.fit(
            X_train,
            y_train_encoded
        )

        # ==================================================
        # VALIDATION
        # ==================================================

        validation_predictions = model.predict(
            X_validation
        )

        validation_accuracy = accuracy_score(
            y_validation_encoded,
            validation_predictions
        )

        print()
        print(
            f"Validation Accuracy: "
            f"{validation_accuracy * 100:.2f}%"
        )

        # ==================================================
        # TEST
        # ==================================================

        test_predictions = model.predict(
            X_test
        )

        test_accuracy = accuracy_score(
            y_test_encoded,
            test_predictions
        )

        print(
            f"Test Accuracy: "
            f"{test_accuracy * 100:.2f}%"
        )

        # ==================================================
        # CLASSIFICATION REPORT
        # ==================================================

        print()
        print("=" * 60)
        print("TEST CLASSIFICATION REPORT")
        print("=" * 60)

        print(
            classification_report(
                y_test_encoded,
                test_predictions,
                target_names=encoder.classes_,
                zero_division=0
            )
        )

        # ==================================================
        # CONFUSION MATRIX
        # ==================================================

        confusion = confusion_matrix(
            y_test_encoded,
            test_predictions
        )

        confusion_path = (
            self.output_dir /
            "confusion_matrix.csv"
        )

        confusion_df = pd.DataFrame(
            confusion,
            index=encoder.classes_,
            columns=encoder.classes_
        )

        confusion_df.to_csv(
            confusion_path
        )

        # ==================================================
        # SAVE MODEL
        # ==================================================

        joblib.dump(
            model,
            self.model_path
        )

        joblib.dump(
            encoder,
            self.encoder_path
        )

        # ==================================================
        # FINAL OUTPUT
        # ==================================================

        print()
        print("=" * 60)
        print("MODEL TRAINING COMPLETED")
        print("=" * 60)

        print(
            f"Model:\n{self.model_path}"
        )

        print(
            f"\nEncoder:\n{self.encoder_path}"
        )

        print(
            f"\nTrees       : {model.n_estimators}"
        )

        print(
            f"Features    : {model.n_features_in_}"
        )

        print(
            f"Classes     : {len(model.classes_)}"
        )

        print(
            f"\nValidation Accuracy: "
            f"{validation_accuracy * 100:.2f}%"
        )

        print(
            f"Test Accuracy      : "
            f"{test_accuracy * 100:.2f}%"
        )

        print(
            f"\nConfusion matrix:\n"
            f"{confusion_path}"
        )

        print("=" * 60)


if __name__ == "__main__":

    trainer = GestureModelTrainer()

    trainer.train()