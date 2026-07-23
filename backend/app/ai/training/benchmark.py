import os
import time
import tracemalloc
import joblib
import pandas as pd

# ==========================================
# Paths
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "random_forest_model.pkl"
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "output",
    "asl_landmarks.csv"
)

REPORT_PATH = os.path.join(
    BASE_DIR,
    "output",
    "benchmark_report.md"
)

# ==========================================
# Load Model
# ==========================================

print("=" * 60)
print("Loading Model...")
print("=" * 60)

model = joblib.load(MODEL_PATH)

print("Model Loaded Successfully!")

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(CSV_PATH)

X = df.drop("label", axis=1)

sample = X.iloc[[0]]

# ==========================================
# Benchmark
# ==========================================

NUM_RUNS = 1000

print("\nRunning Benchmark...")

tracemalloc.start()

start = time.perf_counter()

for _ in range(NUM_RUNS):
    model.predict(sample)

end = time.perf_counter()

current_memory, peak_memory = tracemalloc.get_traced_memory()

tracemalloc.stop()

# ==========================================
# Metrics
# ==========================================

total_time = end - start

average_time_ms = (total_time / NUM_RUNS) * 1000

throughput = NUM_RUNS / total_time

model_size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)

peak_memory_mb = peak_memory / (1024 * 1024)

# ==========================================
# Display
# ==========================================

print("\n" + "=" * 60)
print("INFERENCE BENCHMARK")
print("=" * 60)

print(f"Average Inference Time : {average_time_ms:.4f} ms")
print(f"Throughput             : {throughput:.2f} predictions/sec")
print(f"Peak Memory            : {peak_memory_mb:.4f} MB")
print(f"Model Size             : {model_size_mb:.2f} MB")

# ==========================================
# Save Report
# ==========================================

report = f"""# Benchmark Report

## Model
Random Forest Classifier

## Results

- Average Inference Time: {average_time_ms:.4f} ms
- Throughput: {throughput:.2f} predictions/second
- Peak Memory Usage: {peak_memory_mb:.4f} MB
- Model Size: {model_size_mb:.2f} MB

## Conclusion

The Random Forest model is suitable for real-time webcam-based sign recognition because it provides low inference latency and high prediction throughput while maintaining a manageable memory footprint.
"""

with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write(report)

print("\nBenchmark report generated successfully!")
print(f"Location: {REPORT_PATH}")