import cv2
from backend.app.ai.hand_tracking.detector import HandDetector


def open_webcam():

    detector = HandDetector()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Cannot access webcam!")
        return

    print("Press Q to quit.")

    while True:

        success, frame = camera.read()

        if not success:
            print("Failed to capture frame.")
            break

        frame = detector.detect_hands(frame)

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()