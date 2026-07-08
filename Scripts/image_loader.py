import cv2
import os


def load_image(image_path):

    if not os.path.exists(image_path):
        print("Image not found!")
        return

    image = cv2.imread(image_path)

    if image is None:
        print("Unable to read image.")
        return

    height, width, channels = image.shape

    print("\n========== IMAGE DETAILS ==========\n")
    print(f"Height   : {height}")
    print(f"Width    : {width}")
    print(f"Channels : {channels}")
    print(f"Image Size : {image.size}")

    cv2.imshow("Loaded Image", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":

    image_path = input("Enter image path: ")

    load_image(image_path)