import os
import time
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# =====================================================
# Locate Dataset
# =====================================================

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
    "hyperparameter_report.csv"
)

# =====================================================
# Check Dataset
# =====================================================

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"Dataset not found!\nExpected Location:\n{CSV_PATH}"
    )

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("HYPERPARAMETER STUDY")
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

# =====================================================
# Hyperparameter Study
# =====================================================

tree_values = [50, 100, 200]

results = []

for trees in tree_values:

    print("\n" + "=" * 40)
    print(f"Training Random Forest ({trees} Trees)")
    print("=" * 40)

    model = RandomForestClassifier(
        n_estimators=trees,
        random_state=42
    )

    start_time = time.time()

    model.fit(X_train, y_train)

    end_time = time.time()

    training_time = end_time - start_time

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    results.append({
        "Number of Trees": trees,
        "Training Time (seconds)": round(training_time, 4),
        "Accuracy": round(accuracy, 4),
        "F1 Score": round(f1, 4)
    })

    print(f"Training Time : {training_time:.4f} seconds")
    print(f"Accuracy      : {accuracy:.4f}")
    print(f"F1 Score      : {f1:.4f}")

# =====================================================
# Save Report
# =====================================================

report_df = pd.DataFrame(results)

report_df.to_csv(REPORT_PATH, index=False)

print("\n" + "=" * 60)
print("HYPERPARAMETER STUDY COMPLETED")
print("=" * 60)

print(report_df)

print(f"\nReport Saved To:\n{REPORT_PATH}")