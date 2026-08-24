import pandas as pd
import json
from pathlib import Path

# Locate project root
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[5]

TRAIN_CSV = PROJECT_ROOT / "train.csv"
VALIDATION_CSV = PROJECT_ROOT / "validation.csv"
TEST_CSV = PROJECT_ROOT / "test.csv"

REPORT_JSON = PROJECT_ROOT / "training_report.json"


def get_class_distribution(df):
    return df.iloc[:, -1].value_counts().sort_index().to_dict()


def main():
    print("Reading dataset splits...")

    train_df = pd.read_csv(TRAIN_CSV)
    val_df = pd.read_csv(VALIDATION_CSV)
    test_df = pd.read_csv(TEST_CSV)

    report = {
        "dataset_summary": {
            "training_samples": len(train_df),
            "validation_samples": len(val_df),
            "test_samples": len(test_df),
            "total_samples": len(train_df) + len(val_df) + len(test_df),
            "feature_dimension": train_df.shape[1] - 1,
            "number_of_classes": train_df.iloc[:, -1].nunique()
        },
        "class_distribution": {
            "training": get_class_distribution(train_df),
            "validation": get_class_distribution(val_df),
            "test": get_class_distribution(test_df)
        }
    }

    with open(REPORT_JSON, "w") as f:
        json.dump(report, f, indent=4)

    print("\nTraining report generated successfully!")
    print(f"\nSaved to:\n{REPORT_JSON}")


if __name__ == "__main__":
    main()