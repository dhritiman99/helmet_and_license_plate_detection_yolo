import streamlit as st
import tempfile
import cv2

from models.detect import annotate_image
from components.violations import show_violations
from models.loader import load_models


def process_video(uploaded_file):

    st.title("🎥 Video Tracking System")

    # Load model once per run (no session_state)
    model = load_models()

    # Confidence slider
    conf_filter = st.slider(
        "Set Confidence Filter",
        0.10, 1.00, 0.30, 0.01
    )

    # -----------------------------
    # UPLOAD HANDLING
    # -----------------------------
    if uploaded_file is None:
        st.warning("Please upload a video.")
        return

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    # -----------------------------
    # CONTROL BUTTONS (LOCAL STATE)
    # -----------------------------
    c1, c2, c3 = st.columns(3)
    with c1:
        run = st.button("▶ Start Video")
    with c2:
        stop = st.button("⏹ Stop Video")
    with c3:
        if st.button("🔄 Reset"):
            st.rerun()

    frame_placeholder = st.empty()
    violation_placeholder = st.empty()

    violations = {}

    # -----------------------------
    # VIDEO PROCESSING
    # -----------------------------
    if run:

        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while cap.isOpened():

            if stop:
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1280, 720))

            # -----------------------------
            # TRACKING (ByteTrack)
            # -----------------------------
            results = model.track(
                frame,
                persist=True,
                conf=conf_filter,
                classes=[0, 1, 2, 3],
                verbose=False
            )

            detections = results[0]

            # -----------------------------
            # ANNOTATION + VIOLATIONS
            # -----------------------------
            annotated_frame, violations = annotate_image(
                frame,
                detections,
                violations
            )



            # -----------------------------
            # DISPLAY FRAME
            # -----------------------------
            frame_placeholder.image(
                annotated_frame,
                channels="RGB"
            )
            if violations:
                with violation_placeholder.container():
                    show_violations(violations, "RGB")

        cap.release()
    


    # -----------------------------
    # RESET (simple local reset)
    # -----------------------------
