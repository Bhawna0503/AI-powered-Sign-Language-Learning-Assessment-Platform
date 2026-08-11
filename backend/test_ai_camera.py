import cv2
from app.ai.ai_engine import predict

cap = cv2.VideoCapture(0)

print("Press SPACE to predict")
print("Press ESC to exit")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    cv2.imshow("AI Camera Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key != 255:
        print("Key Pressed:", key)

    if key == 32:      # SPACE

        print("SPACE DETECTED")

        result = predict(frame)

        print("\n========== RESULT ==========")
        print("Prediction :", result.predicted_label)
        print("Confidence :", result.confidence)
        print("Message    :", result.message)
        print("============================\n")

    elif key == 27:    # ESC

        print("ESC DETECTED")
        break

cap.release()
cv2.destroyAllWindows()