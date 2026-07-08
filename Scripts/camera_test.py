import cv2


def main():

    # Open webcam
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Unable to open webcam.")
        return

    print("Press Q to quit.")

    while True:

        success, frame = camera.read()

        if not success:
            print("Failed to capture frame.")
            break

        # Show webcam feed
        cv2.imshow("Webcam Verification", frame)

        # Exit when Q is pressed
        key = cv2.waitKey(1)

        if key == ord("q") or key == ord("Q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()