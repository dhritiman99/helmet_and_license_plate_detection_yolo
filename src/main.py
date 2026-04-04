from ultralytics import YOLO
import cv2

breakpoint()
model = YOLO("src/model/best.pt")
input_source = "public/video3.mp4"

# Mapping: Adjust these IDs based on your model.yaml
# HEAD = 0, HELMET = 1, RIDER = 2, PLATE = 3
HELMET_ID = 0
RIDER_ID = 1
NO_HELMET_ID = 2
PLATE_ID = 3


results = model.track(
    source=input_source,
    stream=True,
    conf=0.6,
    imgsz=(640,480),
    classes = [RIDER_ID, NO_HELMET_ID]
    )

for result in results:
    
    frame = result.orig_img.copy()
    boxes = result.boxes
    
    # 1. Extract all detected objects for this frame
    riders = [b for b in boxes if int(b.cls) == RIDER_ID]
    helmets = [b for b in boxes if int(b.cls) == HELMET_ID]
    no_helmets = [b for b in boxes if int(b.cls) == NO_HELMET_ID]
    plates = [b for b in boxes if int(b.cls) == PLATE_ID]

    for rider in riders:
        r_coords = rider.xyxy[0].tolist() # [x1, y1, x2, y2]
        # Check if any helmet box overlaps with this rider's upper half
        without_helmet = any(
            h.xyxy[0][0] > r_coords[0] and h.xyxy[0][2] < r_coords[2] 
            for h in no_helmets
        )

        if without_helmet:
            # LOGIC TRIGGERED: No helmet found for this specific rider
            

            cv2.putText(
                        frame,
                        "NO HELMET",
                        (int(r_coords[0]), int(r_coords[1] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                        2
            )
            cv2.rectangle(
                frame,
                (int(r_coords[0]), int(r_coords[1])),
                (int(r_coords[2]), int(r_coords[3])),
                (255,0,0),
                2
             )
            # Find the plate belonging to this rider (closest box)
            for plate in plates:
                p_coords = plate.xyxy[0].tolist()
                # Check if plate is within or very near the rider box
                if p_coords[0] > r_coords[0] - 50 and p_coords[2] < r_coords[2] + 50:
                    cv2.rectangle(frame, (int(p_coords[0]), int(p_coords[1])), 
                                  (int(p_coords[2]), int(p_coords[3])), (0, 255, 0), 3)
                    print(f"Captured Violation: Plate found for Rider at {p_coords}")

    frame_display = cv2.resize(frame, (1280, 720)) 
    cv2.imshow("YOLO Violation Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
