import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_FILE = Path(__file__).resolve()

# app/ai/ml/preprocessing/split_dataset.py
#
# parents[0] = preprocessing
# parents[1] = ml
# parents[2] = ai
# parents[3] = app
# parents[4] = backend

PROJECT_ROOT = CURRENT_FILE.parents[4]

OUTPUT_DIR = PROJECT_ROOT / "output"

INPUT_CSV = OUTPUT_DIR / "normalized_landmarks.csv"

TRAIN_CSV = OUTPUT_DIR / "train.csv"
VALIDATION_CSV = OUTPUT_DIR / "validation.csv"
TEST_CSV = OUTPUT_DIR / "test.csv"


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("SPLITTING NORMALIZED DATASET")
    print("=" * 60)

    print(f"Project root : {PROJECT_ROOT}")
    print(f"Input        : {INPUT_CSV}")

    # --------------------------------------------------------
    # Check input
    # --------------------------------------------------------

    if not INPUT_CSV.exists():

        raise FileNotFoundError(
            f"\nNormalized dataset not found:\n"
            f"{INPUT_CSV}\n\n"
            f"Run this first:\n"
            f"python -m app.ai.ml.preprocessing.normalize_landmarks"
        )

    # --------------------------------------------------------
    # Read dataset
    # --------------------------------------------------------

    df = pd.read_csv(INPUT_CSV)

    print()
    print(f"Dataset shape : {df.shape}")

    # --------------------------------------------------------
    # Validate dataset
    # --------------------------------------------------------

    if df.shape[1] != 64:

        raise ValueError(
            f"Expected 64 columns "
            f"(63 features + 1 label), "
            f"but found {df.shape[1]}"
        )

    X = df.iloc[:, :-1]

    y = df.iloc[:, -1]

    print(f"Features      : {X.shape[1]}")
    print(f"Classes       : {y.nunique()}")
    print(
        f"Labels        : "
        f"{sorted(y.astype(str).unique().tolist())}"
    )

    # ========================================================
    # 70% TRAIN / 30% TEMPORARY
    # ========================================================

    X_train, X_temp, y_train, y_temp = train_test_split(

        X,
        y,

        test_size=0.30,

        stratify=y,

        random_state=42
    )

    # ========================================================
    # 15% VALIDATION / 15% TEST
    # ========================================================

    X_validation, X_test, y_validation, y_test = (
        train_test_split(

            X_temp,
            y_temp,

            test_size=0.50,

            stratify=y_temp,

            random_state=42
        )
    )

    # ========================================================
    # RECREATE DATAFRAMES
    # ========================================================

    train_df = pd.concat(
        [
            X_train,
            y_train
        ],
        axis=1
    )

    validation_df = pd.concat(
        [
            X_validation,
            y_validation
        ],
        axis=1
    )

    test_df = pd.concat(
        [
            X_test,
            y_test
        ],
        axis=1
    )

    # ========================================================
    # SAVE
    # ========================================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    train_df.to_csv(
        TRAIN_CSV,
        index=False
    )

    validation_df.to_csv(
        VALIDATION_CSV,
        index=False
    )

    test_df.to_csv(
        TEST_CSV,
        index=False
    )

    # ========================================================
    # RESULTS
    # ========================================================

    print()
    print("=" * 60)
    print("DATASET SPLIT COMPLETED")
    print("=" * 60)

    print(
        f"Training samples   : {len(train_df)}"
    )

    print(
        f"Validation samples : {len(validation_df)}"
    )

    print(
        f"Test samples       : {len(test_df)}"
    )

    print()
    print("Expected shapes:")

    print(
        f"Train       : {train_df.shape}"
    )

    print(
        f"Validation  : {validation_df.shape}"
    )

    print(
        f"Test        : {test_df.shape}"
    )

    # ========================================================
    # CLASS DISTRIBUTION
    # ========================================================

    print()
    print("=" * 60)
    print("CLASS DISTRIBUTION")
    print("=" * 60)

    print("\nTRAIN:")
    print(
        y_train.value_counts()
        .sort_index()
    )

    print("\nVALIDATION:")
    print(
        y_validation.value_counts()
        .sort_index()
    )

    print("\nTEST:")
    print(
        y_test.value_counts()
        .sort_index()
    )

    # ========================================================
    # FILE LOCATIONS
    # ========================================================

    print()
    print("=" * 60)
    print("FILES CREATED")
    print("=" * 60)

    print(
        f"Train:\n{TRAIN_CSV}"
    )

    print(
        f"\nValidation:\n{VALIDATION_CSV}"
    )

    print(
        f"\nTest:\n{TEST_CSV}"
    )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()