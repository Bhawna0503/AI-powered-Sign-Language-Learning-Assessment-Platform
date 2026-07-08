import cv2


class Camera:
    def __init__(self, camera_index=0):
        """
        Initialize webcam.
        camera_index = 0 means default webcam.
        """
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise Exception("❌ Unable to open webcam.")

    def read_frame(self):
        """
        Read one frame.
        Returns:
            success -> bool
            frame -> image
        """
        return self.cap.read()

    def release(self):
        """
        Release webcam resources.
        """
        self.cap.release()
        cv2.destroyAllWindows()