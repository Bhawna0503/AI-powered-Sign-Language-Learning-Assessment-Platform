import os
import pandas as pd

from sklearn.model_selection import train_test_split

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

INPUT_CSV = os.path.join(
    BASE_DIR,
    "output",
    "normalized_landmarks.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

TRAIN_CSV = os.path.join(OUTPUT_DIR, "train.csv")
VALIDATION_CSV = os.path.join(OUTPUT_DIR, "validation.csv")
TEST_CSV = os.path.join(OUTPUT_DIR, "test.csv")

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("SPLITTING DATASET")
print("=" * 60)

df = pd.read_csv(INPUT_CSV)

print(f"Total Samples : {len(df)}")

# =====================================================
# First Split
# 80% Train
# 20% Temporary
# =====================================================

train_df, temp_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)

# =====================================================
# Second Split
# 10% Validation
# 10% Test
# =====================================================

validation_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42,
    stratify=temp_df["label"]
)

# =====================================================
# Save CSV Files
# =====================================================

train_df.to_csv(TRAIN_CSV, index=False)
validation_df.to_csv(VALIDATION_CSV, index=False)
test_df.to_csv(TEST_CSV, index=False)

print("\nDataset Split Completed Successfully!")

print(f"Train Samples      : {len(train_df)}")
print(f"Validation Samples : {len(validation_df)}")
print(f"Test Samples       : {len(test_df)}")

# =====================================================
# Verify Class Distribution
# =====================================================

print("\n" + "=" * 60)
print("CLASS DISTRIBUTION")
print("=" * 60)

print("\nTrain Dataset")
print(train_df["label"].value_counts().sort_index())

print("\nValidation Dataset")
print(validation_df["label"].value_counts().sort_index())

print("\nTest Dataset")
print(test_df["label"].value_counts().sort_index())