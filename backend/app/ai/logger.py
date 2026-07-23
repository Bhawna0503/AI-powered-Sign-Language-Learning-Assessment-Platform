import logging
import os

# ==========================================
# Create Logs Directory
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "inference.log")

# ==========================================
# Configure Logger
# ==========================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class InferenceLogger:
    """
    Logs inference metadata.
    """

    def log_prediction(
        self,
        predicted_label,
        confidence,
        inference_time,
        model_version
    ):

        logging.info(
            f"Prediction={predicted_label} | "
            f"Confidence={confidence:.4f} | "
            f"InferenceTime={inference_time:.2f} ms | "
            f"ModelVersion={model_version}"
        )