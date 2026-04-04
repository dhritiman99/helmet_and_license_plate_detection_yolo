from PIL import Image
import numpy as np

def upload_to_frame(upload):
    img = Image.open(upload)
    img = img.convert("RGB")  # YOLO expects RGB
    frame = np.array(img)      # H x W x 3 NumPy array
    return frame


    """
    Draws bounding boxes and labels on the image.
    
    Parameters:
        frame: np.ndarray (H x W x 3, RGB)
        detections: list of dicts with keys:
            - 'bbox': (x1, y1, x2, y2)
            - 'label': str
            - 'confidence': float
    
    Returns:
        annotated: np.ndarray with drawn boxes and labels
    """
    annotated = frame.copy()

    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        label = det['label']
        conf = det['confidence']

        # Draw bounding box (green)
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

        # Prepare label text
        text = f"{label}: {conf:.2f}"
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

        # Draw filled rectangle as background for text
        cv2.rectangle(annotated, (x1, y1 - text_height - 5), (x1 + text_width, y1), (0, 255, 0), -1)

        # Put text on top
        cv2.putText(annotated, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    return annotated