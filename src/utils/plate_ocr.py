import easyocr
import numpy
from .image import buffer_to_img


def detect_no_plate_text(image):
    image = buffer_to_img(image)
    
    reader = easyocr.Reader(['en']) 
    ocr_res = reader.readtext(image)
    
    if not ocr_res:
        return ""
        
    text_parts = [res[1] for res in ocr_res]

    full_text = "".join(text_parts)
    
    return full_text.upper().strip()