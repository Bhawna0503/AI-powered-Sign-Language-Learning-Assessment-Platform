import cv2

from app.ai.ai_engine import predict


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to open webcam.")
        return

    print("Live recognition started. Press ESC to exit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame.")
            break

        # Predict gesture
        result = predict(frame)

        if result.success:
            text = f"{result.predicted_label} ({result.confidence:.2f})"
            color = (0, 255, 0)
        else:
            text = result.message
            color = (0, 0, 255)

        # Display prediction
        cv2.putText(
            frame,
            text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
        )

        cv2.imshow("Live Sign Language Recognition", frame)

        # ESC key to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()