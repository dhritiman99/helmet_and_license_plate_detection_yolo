import streamlit as st 
import tempfile
from models.detect import detect_from_image, annotate_image
from utils.frame import upload_to_frame
from components.violations import show_violations
from utils.plate_ocr import detect_no_plate_text
import cv2
from utils.image import buffer_to_img

def process_image(upload):

    conf_filter = st.sidebar.slider(
        "Set Confidence Filter",
        min_value=0.10,
        max_value=1.00,
        value=0.40,
        step=0.01,
    )
    detect_button_pressed = st.sidebar.button("Detect")
    with st.container(height=400):
        frame_placeholder = st.empty()

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(upload.read())

    frame_placeholder.image(upload)
    
    if detect_button_pressed:
        with st.spinner(text="Detecting"):
            frame_placeholder.empty()
            
            frame = upload_to_frame(upload)
            detections = detect_from_image(frame, conf_filter)
            annotated_frame, violations = annotate_image(frame, detections)
            for id in violations.keys(): 
                cv2.imwrite('debug.jpg',buffer_to_img(violations[id]['plate_img']))
                text = detect_no_plate_text(violations[id]['plate_img'])
                violations[id]['plate_txt'] = text
            
            show_violations(violations)
            frame_placeholder.image(annotated_frame, channels="BGR")
