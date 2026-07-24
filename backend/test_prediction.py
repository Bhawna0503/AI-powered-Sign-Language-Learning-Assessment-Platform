import cv2

from app.ai.ai_engine import predict

image_path = "../captures/test.jpg"   # or "captures/test.jpg" if you move the image

image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

result = predict(image)

print(result)
