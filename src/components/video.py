import streamlit as st
import tempfile
import cv2
from models.detect import annotate_image
from components.violations import show_violations
from models.loader import load_models
from PIL import Image
from utils.image import preprocess_img
from utils.plate_ocr import detect_no_plate_text
from db.schemas.violation import add_violations

def process_video(uploaded_file):
    if "roi_coords" not in st.session_state:
        st.session_state.roi_coords = None

    model = load_models()

    conf_filter = st.sidebar.slider(
        "Set Confidence Filter",
        0.10, 1.00, 0.30, 0.01
    )

    skip_frames = st.sidebar.slider(
        "Skip Frames",
        1, 20,
        3,
        1
    )

    (v_width, v_height) = st.sidebar.selectbox(
        "Resolution",
        options=[(1280, 720), (1920, 1080), (800, 600)],
        format_func=lambda x: f"{x[0]}x{x[1]}"
    )


    # UPLOAD HANDLING
    if uploaded_file is None:
        st.warning("Please upload a video.")
        return

    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name


    # CONTROL BUTTONS (LOCAL STATE)
    c1, c2, c3 = st.columns(3)
    with c1:
        run = st.button("▶ Start Video")
    with c2:
        stop = st.button("⏹ Stop Video")
    with c3:
        if st.button("Reset"):
            st.session_state.clear()
            st.rerun()
    

    violations = {}
    frame_placeholder = st.empty()
    violation_placeholder = st.empty()
    
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    if st.session_state.roi_coords is None:
        select_roi(cap, v_width, v_height)
        return 

    x1, y1, x2, y2 = st.session_state.roi_coords

    # VIDEO PROCESSING
    if run:
        frame_index = 0
        while cap.isOpened():

            if stop:
                break

            ret, frame = cap.read()
            if not ret:
                break
            if frame_index % skip_frames == 0:
                frame = cv2.resize(frame, (v_width, v_height))
                # TRACKING
                results = model.track(
                    preprocess_img(frame[y1:y2, x1:x2]),
                    persist=True,
                    conf=conf_filter,
                    classes=[0, 1, 2, 3],
                    verbose=False
                )

                detections = results[0]

                # ANNOTATION + VIOLATIONS
                annotated_frame, violations = annotate_image(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    detections,
                    violations,
                    roi_x1=x1, roi_y1=y1, roi_x2=x2, roi_y2=y2
                )
                # DISPLAY FRAME
                frame_placeholder.image(
                    annotated_frame,
                    channels="BGR"
                )

                for id in violations.keys(): 
                    text = detect_no_plate_text(violations[id]['plate_img'])
                    violations[id]['plate_txt'] = text
                
                if violations:
                    with violation_placeholder.container():
                        show_violations(violations, "BGR")
            frame_index += 1
        cap.release()
        with st.spinner("saving violations..."):
            add_violations(violations)
    


def select_roi(cap, v_width, v_height):
    # 1. Get a sample frame for the preview
    ret, frame = cap.read()
    frame = cv2.resize(frame, (v_width, v_height))
    if not ret:
        st.error("Failed to load video preview.")
        return None
    
    # Get video dimensions
    height, width, _ = frame.shape
    st.subheader("Adjust Detection Zone")
    x_range = st.slider("Horizontal Range (X)", 1, width, (0, width))
    y_range = st.slider("Vertical Range (Y)", 1, height, (0, height))
    confirm = st.button("Confirm")
    # 3. Extract coordinates
    x1, x2 = x_range
    y1, y2 = y_range

    # 4. Live Preview
    preview_frame = frame.copy()
    cv2.rectangle(preview_frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    # Label the ROI
    cv2.putText(preview_frame, "DETECTION ZONE", (x1 + 10, y1 + 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    st.image(cv2.cvtColor(preview_frame, cv2.COLOR_BGR2RGB), width=600)

    if confirm:
        st.session_state.roi_coords = (x1, y1, x2, y2)
        st.rerun()

    return None


