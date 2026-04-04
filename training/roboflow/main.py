from ultralytics import YOLO
import cv2

helmet_model = YOLO("src/model/helmet.pt")
plate_model = YOLO("src/model/license_plate.pt")

input_source = "public/video3.mp4"

helmet_results = helmet_model(
    source=input_source,
    stream=True,
    device="cuda",
    conf=0.6
)

plate_results = plate_model(
    source=input_source,
    stream=True,
    device="cuda",
    conf=0.3
)

for p,h in zip(plate_results, helmet_results):
    frame = h.orig_img

    frame = h.plot(img=frame)   # helmet detections
    frame = p.plot(img=frame)   # license plate detections

    cv2.imshow("Multi-Model Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
