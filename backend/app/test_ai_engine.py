import cv2
import time

from ai_engine.predictor import Predictor

predictor = Predictor()

expected = predictor.practice.current_letter()
print(f"Practice Letter: {expected}")

cap = cv2.VideoCapture(0)

start_time = time.time()
frame_count = 0
fps = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1
    elapsed = time.time() - start_time

    if elapsed >= 1:
        fps = frame_count / elapsed
        frame_count = 0
        start_time = time.time()

    result = predictor.predict(frame)

    if result is None:

        cv2.putText(
            frame,
            "Waiting for stable hand...",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        cv2.imshow("AI Engine Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        continue

    print(result)

    expected = predictor.practice.current_letter()

    cv2.putText(
        frame,
        f"Expected: {expected}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"{result.label} ({result.confidence:.2f})",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # Show assessment result
    correct = predictor.progress.history[-1]["correct"] if predictor.progress.history else False

    color = (0, 255, 0) if correct else (0, 0, 255)

    cv2.putText(
        frame,
        "CORRECT" if correct else "INCORRECT",
        (20, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.putText(
        frame,
        f"Confidence: {result.confidence:.2f}",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    cv2.imshow("AI Engine Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()