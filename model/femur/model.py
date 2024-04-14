import cv2
import numpy as np

from utils.utils import predict_and_save


def save_examine_image(image_path, result, x, y, w, h):
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle with thickness 2
    cv2.line(result, (x, y), (x + w, y + h), (0, 255, 0), 2)  # White diagonal line with thickness 2
    cv2.imwrite(image_path, result)


def predict_femur_length(filename, pixel_depth):
    image_path = predict_and_save(filename)

    if image_path is None:
        return None

    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to separate background from the white circle
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Find contours and hierarchy
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the bounding rectangle of the contour (assuming only one contour)
    x, y, w, h = cv2.boundingRect(contours[0])

    # Draw the bounding rectangle and center ellipse on a copy of the original image
    save_examine_image(image_path, image, x, y, w, h)

    # Diagonal length of the rectangle
    diagonal_length = np.sqrt(w ^ 2 + h ^ 2)

    # Actual length in mm
    femur_length = diagonal_length * pixel_depth

    age_1 = (0.004 * pow(femur_length, 2)) + (0.057 * femur_length) + 12.053
    cm = femur_length / 10
    age_2 = (0.262 * pow(cm, 2)) + (2 * cm) + 11.5
    print((age_1 + age_2) / 2)

    return femur_length
