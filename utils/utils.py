import os
from pathlib import Path
from ultralytics import YOLO
import cv2

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / 'media'


def predict_and_save(filename):
    image_path = f'{MEDIA_DIR}/{filename}'
    image = cv2.imread(image_path)
    H, W, _ = image.shape

    model = YOLO(f'{BASE_DIR}/static/model.pt')
    results = model(image)
    for i, result in enumerate(results):
        if result.masks is not None:
            for j, mask in enumerate(result.masks.data):
                mask = mask.cpu().numpy() * 255
                mask = cv2.resize(mask, (W, H))
                cv2.imwrite(image_path, mask)
                return image_path
        else:
            return None

    return None

