import streamlit as st
import cv2
from ultralytics import YOLO
import tempfile
import numpy as np
import os

model_path = os.path.join('detection_module','src','model','best.pt')

st.set_page_config(page_title="Helmet Violation Detection", layout="wide")
st.title("🚦 Helmet & License Plate Violation Detection")

@st.cache_resource
def load_model():
    breakpoint()
    return YOLO(model_path)

if "running" not in st.session_state:
    st.session_state.running = False
if "model" not in st.session_state:
    st.session_state.model = load_model()
if "violated_riders" not in st.session_state:
    st.session_state.violated_riders = set()
if "violations" not in st.session_state:
    st.session_state.violations = {}

model = st.session_state.model

HELMET_ID = 0
RIDER_ID = 1
NO_HELMET_ID = 2
PLATE_ID = 3

uploaded_file = st.file_uploader(
    "Upload Traffic Video or Image",
    type=["mp4", "avi", "mov", "jpg", "jpeg", "png"]
)

col1, col2 = st.columns(2)
with col1:
    start_btn = st.button("▶ Start Detection")
with col2:
    stop_btn = st.button("⏹ Stop Detection")

if start_btn:
    st.session_state.running = True

if stop_btn:
    st.session_state.running = False
    st.session_state.violated_riders = set()
    st.session_state.violations = {}
    st.cache_resource.clear()
    st.cache_data.clear()
    if "model" in st.session_state:
        del st.session_state["model"]
    st.success("Detection stopped. Cache cleared.")
    st.experimental_rerun()

frame_placeholder = st.empty()

def get_rider_id(box):
    rider_id_raw = getattr(box, "id", None)
    if rider_id_raw is None:
        return None
    try:
        if hasattr(rider_id_raw, "item"):
            return int(rider_id_raw.item())
        else:
            return int(rider_id_raw)
    except Exception:
        return None

if uploaded_file is not None and st.session_state.running:

    file_ext = uploaded_file.name.split(".")[-1].lower()

    if file_ext in ["jpg", "jpeg", "png"]:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        results = model.track(img, conf=0.6, imgsz=(640, 480),
                              classes=[RIDER_ID, NO_HELMET_ID, PLATE_ID])

        for result in results:
            frame = result.orig_img.copy()
            boxes = result.boxes
            riders = [b for b in boxes if int(b.cls) == RIDER_ID]
            no_helmets = [b for b in boxes if int(b.cls) == NO_HELMET_ID]
            plates = [b for b in boxes if int(b.cls) == PLATE_ID]

            for rider in riders:
                rider_id = get_rider_id(rider)
                if rider_id is None:
                    continue

                x1, y1, x2, y2 = map(int, rider.xyxy[0].tolist())

                without_helmet = any(
                    h.xyxy[0][0] > x1 and h.xyxy[0][2] < x2 for h in no_helmets
                )

                if without_helmet:
                    overlapping_no_helmets = [
                        h for h in no_helmets if h.xyxy[0][0] > x1 and h.xyxy[0][2] < x2
                    ]
                    max_conf = max([float(h.conf) for h in overlapping_no_helmets]) if overlapping_no_helmets else 0

                    # Crop rider and draw boxes on crop
                    rider_crop = frame[y1:y2, x1:x2].copy()

                    # Draw no helmet boxes relative to crop
                    for h in no_helmets:
                        hx1, hy1, hx2, hy2 = map(int, h.xyxy[0].tolist())
                        if hx1 > x1 and hx2 < x2 and hy1 > y1 and hy2 < y2:
                            rx1, ry1 = hx1 - x1, hy1 - y1
                            rx2, ry2 = hx2 - x1, hy2 - y1
                            cv2.rectangle(rider_crop, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)

                    # Draw plate boxes relative to crop
                    for plate in plates:
                        px1, py1, px2, py2 = map(int, plate.xyxy[0].tolist())
                        if px1 > x1 - 50 and px2 < x2 + 50 and py1 > y1 - 50 and py2 < y2 + 50:
                            rx1, ry1 = px1 - x1, py1 - y1
                            rx2, ry2 = px2 - x1, py2 - y1
                            cv2.rectangle(rider_crop, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)

                    rider_crop_rgb = cv2.cvtColor(rider_crop, cv2.COLOR_BGR2RGB)

                    if (rider_id not in st.session_state.violations) or (max_conf > st.session_state.violations[rider_id]["conf"]):
                        st.session_state.violations[rider_id] = {
                            "img": rider_crop_rgb,
                            "conf": max_conf
                        }

            frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

    elif file_ext in ["mp4", "avi", "mov"]:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_file.getbuffer())
        video_path = tfile.name

        results = model.track(
            source=video_path,
            stream=True,
            conf=0.6,
            imgsz=(640, 480),
            classes=[RIDER_ID, NO_HELMET_ID, PLATE_ID]
        )

        for result in results:
            if not st.session_state.running:
                break

            frame = result.orig_img.copy()
            boxes = result.boxes
            riders = [b for b in boxes if int(b.cls) == RIDER_ID]
            no_helmets = [b for b in boxes if int(b.cls) == NO_HELMET_ID]
            plates = [b for b in boxes if int(b.cls) == PLATE_ID]

            for rider in riders:
                rider_id = get_rider_id(rider)
                if rider_id is None:
                    continue

                x1, y1, x2, y2 = map(int, rider.xyxy[0].tolist())

                without_helmet = any(
                    h.xyxy[0][0] > x1 and h.xyxy[0][2] < x2 for h in no_helmets
                )

                if without_helmet:
                    overlapping_no_helmets = [
                        h for h in no_helmets if h.xyxy[0][0] > x1 and h.xyxy[0][2] < x2
                    ]
                    max_conf = max([float(h.conf) for h in overlapping_no_helmets]) if overlapping_no_helmets else 0

                    rider_crop = frame[y1:y2, x1:x2].copy()

                    for h in no_helmets:
                        hx1, hy1, hx2, hy2 = map(int, h.xyxy[0].tolist())
                        if hx1 > x1 and hx2 < x2 and hy1 > y1 and hy2 < y2:
                            rx1, ry1 = hx1 - x1, hy1 - y1
                            rx2, ry2 = hx2 - x1, hy2 - y1
                            cv2.rectangle(rider_crop, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)

                    for plate in plates:
                        px1, py1, px2, py2 = map(int, plate.xyxy[0].tolist())
                        if px1 > x1 - 50 and px2 < x2 + 50 and py1 > y1 - 50 and py2 < y2 + 50:
                            rx1, ry1 = px1 - x1, py1 - y1
                            rx2, ry2 = px2 - x1, py2 - y1
                            cv2.rectangle(rider_crop, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)

                    rider_crop_rgb = cv2.cvtColor(rider_crop, cv2.COLOR_BGR2RGB)

                    if (rider_id not in st.session_state.violations) or (max_conf > st.session_state.violations[rider_id]["conf"]):
                        st.session_state.violations[rider_id] = {
                            "img": rider_crop_rgb,
                            "conf": max_conf
                        }

            frame_placeholder.image(cv2.resize(frame, (1280, 720))[:, :, ::-1], channels="RGB")

if st.session_state.violations:
    st.subheader("🚨 All Detected Violations")
    violation_items = list(st.session_state.violations.items())
    row_size = 3
    for i in range(0, len(violation_items), row_size):
        cols = st.columns(row_size)
        for j, (r_id, data) in enumerate(violation_items[i:i + row_size]):
            with cols[j]:
                st.image(data["img"], caption=f"Rider ID: {r_id}  Conf: {data['conf']:.2f}", use_column_width=True)