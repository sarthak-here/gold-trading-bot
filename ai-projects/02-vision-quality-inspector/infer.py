def load_image(path: str):
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError(
            "OpenCV is not installed. Install requirements.txt to use image inference."
        ) from exc

    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Could not read image: {path}")
    return img


def predict_defect_stub(path: str) -> dict:
    _ = load_image(path)
    # Placeholder classifier output
    return {"label": "normal", "confidence": 0.61}
