from .loader import load_models
import cv2

def detect_from_image(image):
    model = load_models()
    result = model(image, classes=[2,3])
    return result



def annotate_image(frame, detections):
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
        classes = det.names
        for box in det.boxes:
            x1, y1, x2, y2 = box.xyxy.tolist()[0]
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)


            label = classes[box.cls.tolist()[0]]
            conf = box.conf.tolist()[0]

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