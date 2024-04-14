import cv2
import numpy as np

from utils.utils import predict_and_save


def save_examine_image(image_path, result, x, y, w, h, center, radius_x, radius_y):
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle with thickness 2
    cv2.ellipse(result, center, (radius_x, radius_y), 0, 0, 360, (255, 255, 255), -1)  # Red ellipse for center
    cv2.imwrite(image_path, result)


def predict_gestational_age(filename, pixel_depth):
    image_path = predict_and_save(filename)

    if image_path is None:
        return None

    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to separate background from the white circle
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Find contours, hierarchy
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the bounding rectangle of the contour (assuming only one contour)
    x, y, w, h = cv2.boundingRect(contours[0])

    # Calculate the center point of the bounding rectangle
    center = (x + w // 2, y + h // 2)

    # Calculate the radii of the ellipse to fit within the rectangle
    radius_x = w // 2
    radius_y = h // 2

    # Draw the bounding rectangle and center ellipse on a copy of the original image
    result = np.zeros_like(image)

    save_examine_image(image_path, result, x, y, w, h, center, radius_x, radius_y)

    # Compute the circumference of the ellipse
    circumference = np.pi * np.sqrt(2 * (radius_x ^ 2 + radius_y ^ 2))

    # Compute the head circumference
    head_circumference = circumference * pixel_depth

    # Compute the gestational age
    gestational_age = 0.0001797*head_circumference*head_circumference + 0.02631*head_circumference + 9.667

    return gestational_age
