import os
import cv2
import json
import pandas as pd
import mediapipe as mp
from tqdm import tqdm

# ==========================
# CONFIGURATION
# ==========================

# CHANGE THIS PATH TO YOUR DATASET LOCATION
DATASET_PATH = r"../dataset"

OUTPUT_DIR = "../output"
REPORT_DIR = "../reports"

OUTPUT_CSV = os.path.join(OUTPUT_DIR, "asl_landmarks.csv")
REPORT_JSON = os.path.join(REPORT_DIR, "dataset_report.json")

# Optional Normalization
NORMALIZE = False

# Supported image formats
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")

# Create output folders if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ==========================
# MEDIAPIPE HANDS
# ==========================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

# ==========================
# VARIABLES
# ==========================

dataset = []
skipped_files = []
class_counts = {}

total_images = 0
successful = 0
failed = 0

# ==========================
# PROCESS DATASET
# ==========================

for label in sorted(os.listdir(DATASET_PATH)):

    class_path = os.path.join(DATASET_PATH, label)

    if not os.path.isdir(class_path):
        continue

    class_counts[label] = 0

    print(f"\nProcessing Class: {label}")

    for filename in tqdm(os.listdir(class_path)):

        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue

        image_path = os.path.join(class_path, filename)

        total_images += 1

        image = cv2.imread(image_path)

        if image is None:
            skipped_files.append(image_path)
            failed += 1
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if not results.multi_hand_landmarks:
            skipped_files.append(image_path)
            failed += 1
            continue

        hand = results.multi_hand_landmarks[0]

        features = []

        if NORMALIZE:
            wrist = hand.landmark[0]

            for lm in hand.landmark:
                features.extend([
                    lm.x - wrist.x,
                    lm.y - wrist.y,
                    lm.z - wrist.z
                ])
        else:
            for lm in hand.landmark:
                features.extend([
                    lm.x,
                    lm.y,
                    lm.z
                ])

        features.append(label)

        dataset.append(features)

        successful += 1
        class_counts[label] += 1

hands.close()

# ==========================
# CREATE CSV
# ==========================

columns = []

for i in range(21):
    columns.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

columns.append("label")

df = pd.DataFrame(dataset, columns=columns)

df.to_csv(OUTPUT_CSV, index=False)

# ==========================
# PRINT SUMMARY
# ==========================

print("\n==============================")
print("DATASET SUMMARY")
print("==============================")

print(f"Total Images               : {total_images}")
print(f"Successful Extractions     : {successful}")
print(f"Failed Detections          : {failed}")
print(f"Number of Classes          : {len(class_counts)}")

print("\nSamples Per Class")

for label, count in class_counts.items():
    print(f"{label:>3} : {count}")

print(f"\nCSV Saved To: {OUTPUT_CSV}")

# ==========================
# SAVE REPORT
# ==========================

report = {
    "total_images": total_images,
    "successful_extractions": successful,
    "failed_detections": failed,
    "number_of_classes": len(class_counts),
    "samples_per_class": class_counts,
    "skipped_files": skipped_files
}

with open(REPORT_JSON, "w") as file:
    json.dump(report, file, indent=4)

print(f"Report Saved To: {REPORT_JSON}")

print("\nDone!")