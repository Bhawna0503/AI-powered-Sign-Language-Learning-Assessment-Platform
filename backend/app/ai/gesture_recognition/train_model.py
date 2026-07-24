import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


class GestureModelTrainer:

    def __init__(self):

        backend_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

        self.dataset_path = os.path.join(
            backend_dir,
            "output",
            "asl_landmarks.csv"
        )

        self.model_dir = os.path.join(
            backend_dir,
            "models"
        )

        os.makedirs(self.model_dir, exist_ok=True)

        self.model_path = os.path.join(
            self.model_dir,
            "random_forest_model.pkl"
        )

        self.encoder_path = os.path.join(
            self.model_dir,
            "label_encoder.pkl"
        )

    def train(self):

        print("=" * 60)
        print("Loading Dataset...")
        print("=" * 60)

        df = pd.read_csv(self.dataset_path)

        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        encoder = LabelEncoder()

        y_encoded = encoder.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded
        )

        print("Training Random Forest...")

        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print()
        print("=" * 60)
        print("MODEL TRAINED SUCCESSFULLY")
        print("=" * 60)
        print(f"Accuracy : {accuracy * 100:.2f}%")
        print()

        print(classification_report(
            y_test,
            predictions,
            target_names=encoder.classes_
        ))

        joblib.dump(model, self.model_path)

        joblib.dump(encoder, self.encoder_path)

        print("=" * 60)
        print("Saved Files")
        print("=" * 60)
        print(self.model_path)
        print(self.encoder_path)


if __name__ == "__main__":

    trainer = GestureModelTrainer()

    trainer.train()