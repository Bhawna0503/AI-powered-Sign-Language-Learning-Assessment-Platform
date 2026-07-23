import os
import time
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================
# Locate Dataset
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "output",
    "asl_landmarks.csv"
)

REPORT_PATH = os.path.join(
    BASE_DIR,
    "output",
    "comparison_report.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "random_forest_model.pkl"
)

os.makedirs(MODEL_DIR, exist_ok=True)

# ==========================================
# Load Dataset
# ==========================================

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv(CSV_PATH)

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

# ==========================================
# Training Function
# ==========================================

results = []


def evaluate_model(name, model):

    print(f"\nTraining {name}...")

    start = time.time()

    model.fit(X_train, y_train)

    end = time.time()

    training_time = end - start

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted"
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted"
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted"
    )

    print(f"Accuracy : {accuracy:.4f}")

    results.append({
        "Algorithm": name,
        "Training Time": round(training_time, 4),
        "Accuracy": round(accuracy, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1 Score": round(f1, 4)
    })


# ==========================================
# Train Models
# ==========================================

decision_tree = DecisionTreeClassifier(
    random_state=42
)

random_forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

svm = SVC()

evaluate_model(
    "Decision Tree",
    decision_tree
)

evaluate_model(
    "Random Forest",
    random_forest
)

evaluate_model(
    "Support Vector Machine",
    svm
)

# ==========================================
# Save Comparison Report
# ==========================================

comparison_df = pd.DataFrame(results)

comparison_df.to_csv(
    REPORT_PATH,
    index=False
)

print("\n" + "=" * 60)
print("Comparison Report Generated Successfully!")
print("=" * 60)

print(comparison_df)

print(f"\nSaved to:\n{REPORT_PATH}")

# ==========================================
# Save Best Model
# ==========================================

print("\n" + "=" * 60)
print("Saving Best Model...")
print("=" * 60)

random_forest.fit(X_train, y_train)

joblib.dump(
    random_forest,
    MODEL_PATH
)

print("Model saved successfully!")

print(f"Model Location : {MODEL_PATH}")

print("\n" + "=" * 60)
print("TRAINING COMPLETED SUCCESSFULLY")
print("=" * 60)