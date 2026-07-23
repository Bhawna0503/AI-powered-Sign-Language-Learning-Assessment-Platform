import os
import cv2
import json
import pandas as pd
import mediapipe as mp
from tqdm import tqdm

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

DATASET_PATH = os.path.join(BASE_DIR, "dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

OUTPUT_CSV = os.path.join(OUTPUT_DIR, "asl_landmarks.csv")
REPORT_JSON = os.path.join(REPORT_DIR, "dataset_report.json")

# Set True if you want wrist-based normalization
NORMALIZE = False

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")

# ==========================================================
# INITIALIZE MEDIAPIPE HANDS
# ==========================================================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

# ==========================================================
# VARIABLES
# ==========================================================

dataset = []

skipped_files = []

class_counts = {}

total_images = 0
successful = 0
failed = 0

print("=" * 60)
print("ASL LANDMARK EXTRACTION")
print("=" * 60)

# ==========================================================
# LOOP THROUGH DATASET FOLDERS
# ==========================================================

for folder in sorted(os.listdir(DATASET_PATH)):

    folder_path = os.path.join(DATASET_PATH, folder)

    if not os.path.isdir(folder_path):
        continue

    # Example:
    # A-samples -> A
    # B-samples -> B

    label = folder.split("-")[0]

    class_counts[label] = 0

    print(f"\nProcessing Folder: {folder}")
    # ==========================================================
# PROCESS ALL IMAGES IN CURRENT FOLDER
# ==========================================================

    for filename in tqdm(os.listdir(folder_path), desc=label):

        # Ignore non-image files
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue

        image_path = os.path.join(folder_path, filename)

        total_images += 1

        # ----------------------------
        # Read Image
        # ----------------------------
        image = cv2.imread(image_path)

        if image is None:
            skipped_files.append(image_path)
            failed += 1
            continue

        # ----------------------------
        # Convert BGR → RGB
        # ----------------------------
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # ----------------------------
        # Detect Hand
        # ----------------------------
        results = hands.process(rgb_image)

        # ----------------------------
        # No hand detected
        # ----------------------------
        if not results.multi_hand_landmarks:

            skipped_files.append(image_path)

            failed += 1

            continue

        # ----------------------------
        # Get First Hand
        # ----------------------------
        hand_landmarks = results.multi_hand_landmarks[0]

        features = []

        # ----------------------------
        # Landmark Extraction
        # ----------------------------
        if NORMALIZE:

            wrist = hand_landmarks.landmark[0]

            for landmark in hand_landmarks.landmark:

                features.extend([
                    landmark.x - wrist.x,
                    landmark.y - wrist.y,
                    landmark.z - wrist.z
                ])

        else:

            for landmark in hand_landmarks.landmark:

                features.extend([
                    landmark.x,
                    landmark.y,
                    landmark.z
                ])

        # ----------------------------
        # Append Class Label
        # ----------------------------
        features.append(label)

        dataset.append(features)

        successful += 1

        class_counts[label] += 1
        # ==========================================================
# CLOSE MEDIAPIPE
# ==========================================================

hands.close()

# ==========================================================
# CREATE CSV COLUMNS
# ==========================================================

columns = []

for i in range(21):
    columns.extend([
        f"x{i}",
        f"y{i}",
        f"z{i}"
    ])

columns.append("label")

# ==========================================================
# SAVE CSV
# ==========================================================

df = pd.DataFrame(dataset, columns=columns)

df.to_csv(OUTPUT_CSV, index=False)

print("\nCSV file saved successfully!")
print(f"Location: {OUTPUT_CSV}")

# ==========================================================
# CREATE REPORT
# ==========================================================

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

print("Report generated successfully!")
print(f"Location: {REPORT_JSON}")
# ==========================================================
# PRINT SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print("DATASET SUMMARY")
print("=" * 60)

print(f"Total Images Processed      : {total_images}")
print(f"Successful Extractions      : {successful}")
print(f"Failed Detections           : {failed}")
print(f"Number of Classes           : {len(class_counts)}")

print("\nSamples Per Class")
print("-" * 30)

for label, count in sorted(class_counts.items()):
    print(f"{label:<5} : {count}")

print("\nSkipped Files")
print("-" * 30)

if skipped_files:
    for file in skipped_files:
        print(file)
else:
    print("No skipped files.")

print("\n" + "=" * 60)
print("LANDMARK EXTRACTION COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"\nCSV File    : {OUTPUT_CSV}")
print(f"Report File : {REPORT_JSON}")