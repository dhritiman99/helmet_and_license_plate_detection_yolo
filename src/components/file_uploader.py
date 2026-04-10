import streamlit as st
import tempfile
import cv2

def process_upload():
    uploaded_file = st.file_uploader(
        "Upload image / video",
        type=['jpg', 'png', 'mp4']
    )

    if uploaded_file is not None:
        file_type = uploaded_file.type

        # Handle Image
        if "image" in file_type:
            st.image(uploaded_file)

        # Handle Video
        elif "video" in file_type:
            # Save uploaded video to a temporary file
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())

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