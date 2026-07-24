import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


class ModelEvaluator:

    def __init__(self):

        backend_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

        self.dataset_path = os.path.join(
            backend_dir,
            "output",
            "asl_landmarks.csv"
        )

        self.model_path = os.path.join(
            backend_dir,
            "models",
            "random_forest_model.pkl"
        )

        self.encoder_path = os.path.join(
            backend_dir,
            "models",
            "label_encoder.pkl"
        )

        self.report_path = os.path.join(
            backend_dir,
            "reports",
            "evaluation_report.txt"
        )

    def evaluate(self):

        print("=" * 60)
        print("Loading Dataset...")
        print("=" * 60)

        df = pd.read_csv(self.dataset_path)

        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        encoder = joblib.load(self.encoder_path)

        y_encoded = encoder.transform(y)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded
        )

        model = joblib.load(self.model_path)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        precision = precision_score(
            y_test,
            predictions,
            average="weighted"
        )

        recall = recall_score(
            y_test,
            predictions,
            average="weighted"
        )

        f1 = f1_score(
            y_test,
            predictions,
            average="weighted"
        )

        report = classification_report(
            y_test,
            predictions,
            target_names=encoder.classes_
        )

        matrix = confusion_matrix(
            y_test,
            predictions
        )

        print()
        print("=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)
        print(f"Accuracy  : {accuracy*100:.2f}%")
        print(f"Precision : {precision:.4f}")
        print(f"Recall    : {recall:.4f}")
        print(f"F1 Score  : {f1:.4f}")

        print()
        print("Classification Report")
        print(report)

        print("Confusion Matrix")
        print(matrix)

        os.makedirs(os.path.dirname(self.report_path), exist_ok=True)

        with open(self.report_path, "w") as f:

            f.write("MODEL EVALUATION REPORT\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Accuracy : {accuracy*100:.2f}%\n")
            f.write(f"Precision : {precision:.4f}\n")
            f.write(f"Recall : {recall:.4f}\n")
            f.write(f"F1 Score : {f1:.4f}\n\n")

            f.write(report)

            f.write("\nConfusion Matrix\n")
            f.write(str(matrix))

        print()
        print("=" * 60)
        print("Evaluation report saved.")
        print(self.report_path)
        print("=" * 60)


if __name__ == "__main__":

    evaluator = ModelEvaluator()

    evaluator.evaluate()