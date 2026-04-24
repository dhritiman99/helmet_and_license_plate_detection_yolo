import easyocr
import numpy
from .image import buffer_to_img, preprocess_img
import streamlit as st

@st.cache_resource
def load_ocr_model():
    return easyocr.Reader(['en'])

def detect_no_plate_text(image):
    image = buffer_to_img(image)
    reader = load_ocr_model()    
    ocr_res = reader.readtext(image)
    
    if not ocr_res:
        return ""
        
    text_parts = [res[1] for res in ocr_res]

    full_text = "".join(text_parts)
    
    return full_text.upper().strip()