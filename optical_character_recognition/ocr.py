from PIL import Image
import pytesseract
import argparse
import cv2
import os


def preprocess_image(image, threshold):
    if not os.path.exists(image):
        raise FileNotFoundError("Image path does not exist")

    # load the image and convert to grayscale
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if threshold is needed to apply
    if threshold == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif threshold == "blur":
        gray = cv2.medianBlur(gray, 3)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    return image, gray, filename


def image_to_string(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("Preprocessed image not found")

    # load the image as PIL image and apply tesseract OCR
    text = pytesseract.image_to_string(Image.open(filename))
    print(text)

    # clean the processed image
    os.remove(filename)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image file")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
    args = vars(ap.parse_args())

    image = args['image']
    threshold = args['preprocess']
    original_image, processed_image, filename = preprocess_image(image, threshold)
    image_to_string(filename)

    # show output image
    cv2.imshow("Image", original_image)
    cv2.imshow("Processed", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
