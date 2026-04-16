import cv2
import numpy

def img_to_buffer(img: numpy.ndarray):
    success, img_buffer = cv2.imencode('.png',img)
    return img_buffer

def buffer_to_img(buffer):
    nparr = numpy.frombuffer(buffer, numpy.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def preprocess_img(image):
    """
    Optimized pipeline for YOLO:
    1. CLAHE (Contrast Enhancement)
    2. Bilateral Filter (Noise reduction with edge preservation)
    3. Unsharp Masking (Edge sharpening)
    """
    if image is None:
        return None

    # --- 1. Contrast Enhancement (CLAHE) ---
    # Improves detection in shadows and bright sunlight
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # --- 2. Noise Reduction (Bilateral Filter) ---
    # Removes compression artifacts/grain without blurring object boundaries
    denoised = cv2.bilateralFilter(enhanced_img, d=5, sigmaColor=50, sigmaSpace=50)

    # --- 3. Sharpening (Unsharp Masking) ---
    # Highlights edges of helmets and license plate characters
    # We use a weighted sum to avoid creating too much 'haloing'
    gaussian_blur = cv2.GaussianBlur(denoised, (0, 0), 3)
    sharpened = cv2.addWeighted(denoised, 1.5, gaussian_blur, -0.5, 0)

    return sharpened