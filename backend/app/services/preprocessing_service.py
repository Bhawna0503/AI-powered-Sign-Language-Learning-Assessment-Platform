import subprocess
import os
import sys


class PreprocessingService:

    def run_preprocessing(self):

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        script_path = os.path.join(
            base_dir,
            "app",
            "ai",
            "utils",
            "extract_landmarks.py"
        )

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(
                f"Preprocessing failed:\n{result.stderr}"
            )

        return {
            "success": True,
            "message": "Dataset preprocessing completed successfully."
        }