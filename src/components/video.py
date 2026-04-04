import streamlit as st 
import tempfile
import cv2

def process_video(upload):
     # Save uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(upload.read())

    cap = cv2.VideoCapture(tfile.name)
    frame_placeholder = st.empty()

    stop = st.button("Stop")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or stop:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame)

    cap.release()