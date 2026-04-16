import numpy as np
import cv2
import supervision as sv
from .loader import load_models
from utils.image import img_to_buffer

# 1. Configuration
CLASS_NAMES = {0: 'helmet', 1: 'motorcyclist', 2: 'no-helmet', 3: 'plate'}
ID_HELMET = 0
ID_MOTORCYCLIST = 1
ID_NO_HELMET = 2
ID_PLATE = 3

CUSTOM_COLOR_LOOKUP = {
    0: sv.Color(r=255, g=0, b=0),     # helmet
    1: sv.Color.WHITE,                # motorcyclist
    2: sv.Color(r=0, g=0, b=255),     # no-helmet
    3: sv.Color.GREEN                 # plate
}

_MODEL = None


def detect_from_image(image, conf):
    global _MODEL
    if _MODEL is None:
        _MODEL = load_models()
    result = _MODEL.track(
    image,
    persist=True,
    classes=[0, 1, 2, 3],
    conf=conf,
    tracker="bytetrack.yaml"
    )[0]
    return result


def crop_image(image, xyxy):
    h, w, _ = image.shape
    x1, y1, x2, y2 = xyxy.astype(int)
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    return image[y1:y2, x1:x2]


def is_inside(inner_box, outer_box):
    cx = (inner_box[0] + inner_box[2]) / 2
    cy = (inner_box[1] + inner_box[3]) / 2
    return (outer_box[0] <= cx <= outer_box[2]) and (outer_box[1] <= cy <= outer_box[3])


def annotate_image(frame, detections, violations=None, roi_x1=0, roi_y1=0, roi_x2=0, roi_y2=0):

    if violations is None:
        violations = {}

    sv_detections = sv.Detections.from_ultralytics(detections)
    if len(sv_detections.xyxy) > 0:
        sv_detections.xyxy += np.array([roi_x1, roi_y1, roi_x1, roi_y1])

    keep_mask = np.array([class_id != ID_PLATE for class_id in sv_detections.class_id])

    riders = sv_detections[sv_detections.class_id == ID_MOTORCYCLIST]
    no_helmets = sv_detections[sv_detections.class_id == ID_NO_HELMET]
    all_plates_indices = np.where(sv_detections.class_id == ID_PLATE)[0]

    for r_idx, rider_box in enumerate(riders.xyxy):
        conf = float(riders.confidence[r_idx])
        has_violation = False

        # check no-helmet inside rider
        for nh_box in no_helmets.xyxy:
            if is_inside(nh_box, rider_box):
                has_violation = True
                break

        if not has_violation:
            continue

        # find closest plate
        best_plate_idx = None
        min_dist = float('inf')

        for p_idx in all_plates_indices:
            p_box = sv_detections.xyxy[p_idx]

            rc = np.array([
                (rider_box[0] + rider_box[2]) / 2,
                (rider_box[1] + rider_box[3]) / 2
            ])
            pc = np.array([
                (p_box[0] + p_box[2]) / 2,
                (p_box[1] + p_box[3]) / 2
            ])

            dist = np.linalg.norm(rc - pc)

            if dist < 400 and dist < min_dist:
                min_dist = dist
                best_plate_idx = p_idx

        if best_plate_idx is None:
            continue

        # keep this plate
        keep_mask[best_plate_idx] = True

        # crops
        rider_crop = crop_image(frame, rider_box)
        plate_crop = crop_image(frame, sv_detections.xyxy[best_plate_idx])

        if riders.tracker_id is not None:
            tracker_id = riders.tracker_id[r_idx]

        if riders.tracker_id is not None:
            if int(tracker_id) not in violations or violations[int(tracker_id)]['conf'] < conf:
                violations[int(tracker_id)] = {
                    "rider_img": img_to_buffer(cv2.cvtColor(rider_crop, cv2.COLOR_BGR2RGB)),
                    "plate_img": img_to_buffer(cv2.cvtColor(plate_crop, cv2.COLOR_BGR2RGB)),
                    "conf": conf
                }

    # filter detections
    sv_detections = sv_detections[keep_mask]

    # annotation
    palette = sv.ColorPalette([CUSTOM_COLOR_LOOKUP[i] for i in range(len(CLASS_NAMES))])
    box_annotator = sv.BoxAnnotator(color=palette, thickness=2)
    label_annotator = sv.LabelAnnotator(
        color=palette,
        text_color=sv.Color.BLACK,
        text_scale=0.5
    )

    labels = [
        f"{CLASS_NAMES.get(class_id, 'Unknown')} {conf:.2f}"
        for class_id, conf in zip(sv_detections.class_id, sv_detections.confidence)
    ]

    annotated_frame = frame.copy()
    cv2.rectangle(
        annotated_frame,
        (roi_x1,roi_y1),(roi_x2, roi_y2),
        (255,0,0),
        2
    )
    annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=sv_detections)
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame,
        detections=sv_detections,
        labels=labels
    )

    return cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB), violations