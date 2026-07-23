import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

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

# ==========================================
# Load Dataset
# ==========================================

print("=" * 50)
print("Loading Dataset...")
print("=" * 50)

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

# ==========================================
# Train Model
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

print("\nTraining Random Forest...")

model.fit(X_train, y_train)

# ==========================================
# Predictions
# ==========================================

y_pred = model.predict(X_test)

# ==========================================
# Confusion Matrix
# ==========================================

labels = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

# ==========================================
# Save Confusion Matrix
# ==========================================

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "output",
    "confusion_matrix.csv"
)

cm_df.to_csv(OUTPUT_PATH)

print("\nConfusion Matrix Generated Successfully!")

print(f"\nSaved to:\n{OUTPUT_PATH}")
# ==========================================
# Find Top 5 Most Confused Gestures
# ==========================================

confusions = []

for i in range(len(labels)):
    for j in range(len(labels)):

        if i == j:
            continue

        count = cm[i][j]

        if count > 0:
            confusions.append({
                "Actual": labels[i],
                "Predicted": labels[j],
                "Count": count
            })

confusions = sorted(
    confusions,
    key=lambda x: x["Count"],
    reverse=True
)

print("\n" + "=" * 60)
print("TOP 5 MOST CONFUSED GESTURES")
print("=" * 60)

for confusion in confusions[:5]:
    print(
        f"{confusion['Actual']} → {confusion['Predicted']} "
        f"({confusion['Count']} times)"
    )