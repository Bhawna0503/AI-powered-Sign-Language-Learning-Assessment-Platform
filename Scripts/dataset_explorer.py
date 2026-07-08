import os
import csv
import json

# ==========================
# Project Paths
# ==========================

# Get project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ASL Dataset
DATASET_PATH = os.path.join(BASE_DIR, "backend", "dataset")

# Reports
REPORTS_DIR = os.path.join(BASE_DIR, "backend", "reports")
REPORT_PATH = os.path.join(REPORTS_DIR, "dataset_report.csv")

# WLASL Annotation File
WLASL_JSON = os.path.join(BASE_DIR, "backend", "WLASL_v0.3.json")


# ==========================
# ASL DATASET EXPLORER
# ==========================

def explore_dataset():

    if not os.path.exists(DATASET_PATH):
        print("Dataset folder not found!")
        print(DATASET_PATH)
        return

    class_counts = {}
    total_images = 0

    for class_name in sorted(os.listdir(DATASET_PATH)):

        class_path = os.path.join(DATASET_PATH, class_name)

        if os.path.isdir(class_path):

            image_count = len([
                file for file in os.listdir(class_path)
                if file.lower().endswith((".jpg", ".jpeg", ".png"))
            ])

            class_counts[class_name] = image_count
            total_images += image_count

    if len(class_counts) == 0:
        print("No class folders found!")
        return

    total_classes = len(class_counts)

    largest_class = max(class_counts, key=class_counts.get)
    smallest_class = min(class_counts, key=class_counts.get)

    print("\n======================================")
    print("        ASL DATASET REPORT")
    print("======================================")

    print(f"\nTotal Classes : {total_classes}")
    print(f"Total Images  : {total_images}")

    print(f"\nLargest Class : {largest_class} ({class_counts[largest_class]} images)")
    print(f"Smallest Class: {smallest_class} ({class_counts[smallest_class]} images)")

    print("\nImages Per Class\n")

    for name, count in class_counts.items():
        print(f"{name:<15} {count}")

    # Create reports folder
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Save CSV
    with open(REPORT_PATH, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Class", "Images"])

        for name, count in class_counts.items():
            writer.writerow([name, count])

    print("\nCSV Saved Successfully!")
    print(REPORT_PATH)


# ==========================
# WLASL DATASET EXPLORER
# ==========================

def explore_wlasl():

    print("\n======================================")
    print("        WLASL DATASET REPORT")
    print("======================================")

    if not os.path.exists(WLASL_JSON):
        print("\nWLASL_v0.3.json not found!")
        print("Expected location:")
        print(WLASL_JSON)
        return

    with open(WLASL_JSON, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"\nTotal Unique Signs : {len(data)}")

    print("\nFirst Five Entries\n")

    for i, sign in enumerate(data[:5], start=1):

        print(f"{i}. Gloss : {sign['gloss']}")

        print(f"   Instances : {len(sign['instances'])}")

        print("-" * 40)


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    explore_dataset()

    explore_wlasl()