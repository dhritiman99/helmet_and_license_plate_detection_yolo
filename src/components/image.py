import streamlit as st 
import tempfile
from models.detect import detect_from_image, annotate_image
from utils.frame import upload_to_frame
from components.violations import show_violations

def process_image(upload):

    detect_button_pressed = st.button("Detect")

    frame_placeholder = st.empty()

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(upload.read())
    
    frame_placeholder.image(upload)

    if detect_button_pressed:
        frame = upload_to_frame(upload)
        detections = detect_from_image(frame)
        annotated_frame, violations = annotate_image(frame, detections)
        
        show_violations(violations)
        frame_placeholder.image(annotated_frame)
