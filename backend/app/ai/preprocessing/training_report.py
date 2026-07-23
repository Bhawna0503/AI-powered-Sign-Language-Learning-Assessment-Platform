import os
import json
import pandas as pd

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

TRAIN_CSV = os.path.join(OUTPUT_DIR, "train.csv")
VALIDATION_CSV = os.path.join(OUTPUT_DIR, "validation.csv")
TEST_CSV = os.path.join(OUTPUT_DIR, "test.csv")

DATASET_REPORT = os.path.join(REPORT_DIR, "dataset_report.json")
TRAINING_REPORT = os.path.join(REPORT_DIR, "training_report.json")

# =====================================================
# Load Datasets
# =====================================================

train_df = pd.read_csv(TRAIN_CSV)
validation_df = pd.read_csv(VALIDATION_CSV)
test_df = pd.read_csv(TEST_CSV)

total_df = pd.concat(
    [train_df, validation_df, test_df],
    ignore_index=True
)

# =====================================================
# Failed Landmark Count
# =====================================================

failed_count = 0

if os.path.exists(DATASET_REPORT):

    with open(DATASET_REPORT, "r") as file:

        dataset_report = json.load(file)

        failed_count = dataset_report.get(
            "failed_detections",
            0
        )

# =====================================================
# Create Report
# =====================================================

report = {

    "total_samples": len(total_df),

    "number_of_gesture_classes": total_df["label"].nunique(),

    "samples_per_class":
        total_df["label"].value_counts().sort_index().to_dict(),

    "number_of_features": 63,

    "training_set_size": len(train_df),

    "validation_set_size": len(validation_df),

    "test_set_size": len(test_df),

    "failed_landmark_extraction_count": failed_count

}

# =====================================================
# Save Report
# =====================================================

os.makedirs(REPORT_DIR, exist_ok=True)

with open(TRAINING_REPORT, "w") as file:
    json.dump(report, file, indent=4)

print("=" * 60)
print("TRAINING REPORT GENERATED SUCCESSFULLY")
print("=" * 60)

print(json.dumps(report, indent=4))

print(f"\nSaved To:\n{TRAINING_REPORT}")