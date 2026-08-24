import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

CURRENT_FILE = Path(__file__).resolve()

# app/ai/ml/preprocessing/normalize_landmarks.py
# parents[0] = preprocessing
# parents[1] = ml
# parents[2] = ai
# parents[3] = app
# parents[4] = backend

PROJECT_ROOT = CURRENT_FILE.parents[4]

INPUT_CSV = PROJECT_ROOT / "output" / "asl_landmarks.csv"
OUTPUT_CSV = PROJECT_ROOT / "output" / "normalized_landmarks.csv"


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_sample(features):
    """
    Normalize one MediaPipe hand landmark sample.

    Input:
        63 raw values
        21 landmarks × (x, y, z)

    Steps:
        1. Convert to 21x3
        2. Make coordinates wrist-relative
        3. Scale by maximum distance from wrist
        4. Return 63 values
    """

    features = np.asarray(
        features,
        dtype=np.float64
    )

    if features.size != 63:
        raise ValueError(
            f"Expected 63 features, got {features.size}"
        )

    landmarks = features.reshape(21, 3)

    # --------------------------------------------------------
    # Wrist landmark = landmark 0
    # --------------------------------------------------------

    wrist = landmarks[0].copy()

    # --------------------------------------------------------
    # Wrist-relative coordinates
    # --------------------------------------------------------

    landmarks = landmarks - wrist

    # --------------------------------------------------------
    # Calculate distance of every landmark from wrist
    # --------------------------------------------------------

    distances = np.linalg.norm(
        landmarks,
        axis=1
    )

    max_distance = np.max(distances)

    # --------------------------------------------------------
    # Avoid division by zero
    # --------------------------------------------------------

    if max_distance > 1e-8:

        landmarks = (
            landmarks / max_distance
        )

    else:

        landmarks = np.zeros_like(
            landmarks
        )

    return landmarks.flatten()


# ============================================================
# CREATE NORMALIZED DATASET
# ============================================================

def main():

    print("=" * 60)
    print("NORMALIZING LANDMARK DATASET")
    print("=" * 60)

    print(f"Input : {INPUT_CSV}")
    print(f"Output: {OUTPUT_CSV}")

    if not INPUT_CSV.exists():

        raise FileNotFoundError(
            f"Input dataset not found:\n{INPUT_CSV}"
        )

    df = pd.read_csv(
        INPUT_CSV
    )

    print(
        f"Original shape: {df.shape}"
    )

    # --------------------------------------------------------
    # Separate features and labels
    # --------------------------------------------------------

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    if X.shape[1] != 63:

        raise ValueError(
            f"Expected 63 features, "
            f"found {X.shape[1]}"
        )

    normalized_data = []

    # --------------------------------------------------------
    # Normalize every sample
    # --------------------------------------------------------

    for index, row in X.iterrows():

        normalized_features = normalize_sample(
            row.values
        )

        normalized_data.append(
            normalized_features
        )

    normalized_X = pd.DataFrame(
        normalized_data,
        columns=X.columns
    )

    normalized_df = pd.concat(
        [
            normalized_X,
            y.reset_index(drop=True)
        ],
        axis=1
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    normalized_df.to_csv(
        OUTPUT_CSV,
        index=False
    )

    print()
    print("Normalization completed.")
    print(
        f"Normalized shape: {normalized_df.shape}"
    )

    print(
        f"Features: {normalized_X.shape[1]}"
    )

    print(
        f"Classes: {y.nunique()}"
    )

    print(
        "Labels:",
        sorted(
            y.astype(str).unique()
        )
    )

    print()
    print(
        "Feature range:"
    )

    print(
        "Min:",
        normalized_X.min().min()
    )

    print(
        "Max:",
        normalized_X.max().max()
    )

    print()
    print(
        f"Saved to:\n{OUTPUT_CSV}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()