import cv2
import time

from ai.hand_tracking.camera import Camera
from ai.hand_tracking.hand_detector import HandDetector
from ai.utils.landmark_extractor import LandmarkExtractor
from ai.utils.json_saver import JsonSaver


def main():

    # Initialize Camera
    try:
        camera = Camera()
    except Exception as error:
        print(error)
        return

    # Initialize Hand Detector
    detector = HandDetector()

    # Initialize Landmark Extractor
    extractor = LandmarkExtractor()

    # Initialize JSON Saver
    saver = JsonSaver()

    # FPS Variables
    previous_time = 0
    current_time = 0

    while True:

        # Read frame
        success, frame = camera.read_frame()

        if not success:
            print("Failed to read frame.")
            break

        # Detect Hands
        frame, results = detector.detect_hands(frame)

        # Extract Landmark Coordinates
        landmarks = extractor.extract_landmarks(results)

        # Print Landmark Coordinates
        if landmarks:

            for hand_index, hand in enumerate(landmarks):

                print("\n=========================")
                print(f"Hand {hand_index + 1}")
                print("=========================")

                for landmark_index, point in enumerate(hand):

                    print(
                        f"Landmark {landmark_index} : "
                        f"x = {point['x']:.4f} "
                        f"y = {point['y']:.4f} "
                        f"z = {point['z']:.4f}"
                    )

        # ---------------- FPS ----------------

        current_time = time.time()

        if previous_time == 0:
            fps = 0
        else:
            fps = 1 / (current_time - previous_time)

        previous_time = current_time

        # ---------------- Hand Count ----------------

        hand_count = 0

        if results.multi_hand_landmarks:
            hand_count = len(results.multi_hand_landmarks)

        # Display FPS
        cv2.putText(
            frame,
            f"FPS : {int(fps)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Display Hands
        cv2.putText(
            frame,
            f"Hands : {hand_count}",
            (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

        # No Hand Detected
        if hand_count == 0:

            cv2.putText(
                frame,
                "No Hand Detected",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # Display Webcam
        cv2.imshow("Hand Tracking", frame)

        # Keyboard Controls
        key = cv2.waitKey(1) & 0xFF

        # Save JSON
        if key == ord("s") or key == ord("S"):

            if landmarks:
                saver.save(landmarks)
            else:
                print("❌ No hand detected. Nothing to save.")

        # Quit
        if key == ord("q") or key == ord("Q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()