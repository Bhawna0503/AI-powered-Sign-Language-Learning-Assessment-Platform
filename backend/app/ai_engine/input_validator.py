import cv2
import numpy as np

class InputValidator:

    def validate(self, image):

        if image is None:
            return False, "No image received."

        if not isinstance(image, np.ndarray):
            return False, "Invalid image format."

        if image.size == 0:
            return False, "Empty image received."

        height, width = image.shape[:2]

        if height < 100 or width < 100:
            return False, "Image quality is too low."

        return True, "Valid input."