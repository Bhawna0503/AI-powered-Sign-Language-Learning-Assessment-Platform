import os
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

INPUT_CSV = os.path.join(
    BASE_DIR,
    "output",
    "asl_landmarks.csv"
)

OUTPUT_CSV = os.path.join(
    BASE_DIR,
    "output",
    "normalized_landmarks.csv"
)

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("NORMALIZING LANDMARK DATASET")
print("=" * 60)

df = pd.read_csv(INPUT_CSV)

# =====================================================
# Normalize Landmarks
# Wrist-relative normalization
# =====================================================

normalized_data = []

for _, row in df.iterrows():

    row = row.copy()

    wrist_x = row["x0"]
    wrist_y = row["y0"]
    wrist_z = row["z0"]

    for i in range(21):

        row[f"x{i}"] = row[f"x{i}"] - wrist_x
        row[f"y{i}"] = row[f"y{i}"] - wrist_y
        row[f"z{i}"] = row[f"z{i}"] - wrist_z

    normalized_data.append(row)

normalized_df = pd.DataFrame(normalized_data)

# =====================================================
# Save Dataset
# =====================================================

normalized_df.to_csv(OUTPUT_CSV, index=False)

print("\nNormalization completed successfully!")

print(f"\nInput File : {INPUT_CSV}")
print(f"Output File: {OUTPUT_CSV}")