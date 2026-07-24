import os
import sys
import time
import cv2
import numpy as np

# -----------------------------------------------------
# Fix Python import path
# -----------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.ai.ai_engine import predict


class Benchmark:
    """
    Measures the inference speed of the AI Engine.
    """

    def __init__(self):

        self.image_path = os.path.join(
            BACKEND_DIR,
            "captures",
            "test.jpg"
        )

    def run(self):

        print("=" * 60)
        print("AI ENGINE BENCHMARK")
        print("=" * 60)

        print(f"Image Path : {self.image_path}")

        if not os.path.exists(self.image_path):
            print("\nERROR: Test image not found!")
            print("Place test.jpg inside backend/captures/")
            return

        image = cv2.imread(self.image_path)

        if image is None:
            print("ERROR: Unable to read image.")
            return

        runs = 50
        inference_times = []

        print(f"\nRunning {runs} inference tests...\n")

        for i in range(runs):

            start = time.perf_counter()

            result = predict(image)

            end = time.perf_counter()

            elapsed = (end - start) * 1000

            inference_times.append(elapsed)

        average = np.mean(inference_times)
        minimum = np.min(inference_times)
        maximum = np.max(inference_times)
        fps = 1000 / average

        print("=" * 60)
        print("BENCHMARK RESULTS")
        print("=" * 60)

        print(f"Average Inference Time : {average:.2f} ms")
        print(f"Minimum Inference Time : {minimum:.2f} ms")
        print(f"Maximum Inference Time : {maximum:.2f} ms")
        print(f"Estimated FPS          : {fps:.2f}")

        print("=" * 60)

        print("\nLast Prediction")
        print(result)

        report_dir = os.path.join(BACKEND_DIR, "reports")
        os.makedirs(report_dir, exist_ok=True)

        report_path = os.path.join(report_dir, "benchmark_report.txt")

        with open(report_path, "w") as f:

            f.write("AI ENGINE BENCHMARK REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Average Inference Time : {average:.2f} ms\n")
            f.write(f"Minimum Inference Time : {minimum:.2f} ms\n")
            f.write(f"Maximum Inference Time : {maximum:.2f} ms\n")
            f.write(f"Estimated FPS          : {fps:.2f}\n\n")
            f.write("Last Prediction\n")
            f.write(str(result))

        print(f"\nBenchmark report saved to:\n{report_path}")


if __name__ == "__main__":

    Benchmark().run()