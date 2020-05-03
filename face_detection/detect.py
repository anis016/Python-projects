import cv2
import os


def load_classifier(filename=None):
    if filename is None:
        raise FileNotFoundError("filename shouldn't be none")

    dirname, _ = os.path.split(os.path.abspath(__file__))
    classifier_dir = os.path.join(dirname, "trained_classifiers")
    classifier_path = os.path.join(classifier_dir, filename)
    if not os.path.exists(classifier_path):
        raise FileExistsError("{0} doesn't exist".format(filename))

    return cv2.CascadeClassifier(classifier_path)


def preprocess_image(image):
    if not os.path.exists(image):
        raise FileExistsError("image path does not exist")

    # load the image and convert to grayscale
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_threshed = cv2.equalizeHist(gray)
    gray_threshed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return image, gray_threshed


def _detect(image):
    face_cascade = load_classifier("haarcascade_frontalface_default.xml")
    image, processed_image = preprocess_image(image)
    detect_face = face_cascade.detectMultiScale(processed_image, scaleFactor=1.1, minNeighbors=4)
    draw_rectangle(image, detect_face, (255, 0, 0))

    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_rectangle(image, rects, color):
    for x, y, w, h in rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)


if __name__ == '__main__':
    image = 'liam_batman.jpg'
    _detect(image)
