import json
import os
from datetime import datetime


class JsonSaver:

    def __init__(self):

        self.capture_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "..",
            "..",
            "captures"
        )

        os.makedirs(self.capture_folder, exist_ok=True)

    def save(self, landmarks):

        existing_files = [
            file for file in os.listdir(self.capture_folder)
            if file.endswith(".json")
        ]

        file_name = f"capture_{len(existing_files)+1:03}.json"

        file_path = os.path.join(self.capture_folder, file_name)

        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hands": []
        }

        for hand_index, hand in enumerate(landmarks):

            hand_data = {
                "hand_number": hand_index + 1,
                "landmarks": hand
            }

            data["hands"].append(hand_data)

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f"\nSaved: {file_name}")