import cv2


def predict_and_save(model, image_path):
    image = cv2.imread(image_path)
    H, W, _ = image.shape

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

