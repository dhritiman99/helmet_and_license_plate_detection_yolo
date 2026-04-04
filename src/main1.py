import cv2
from ultralytics import YOLO
import os 

model_path = os.path.join('src','model','best.pt')
input = os.path.join('public','video1.mp4')
model = YOLO(model_path)
video_capture = cv2.VideoCapture(input)

violations = []
class_ids = {'helmet':0, 'motorcyclist':1, 'no-helmet':2, 'plate':3}

results = model.track(
    input,
    stream=True,
    imgsz=(640,480),
    conf=0.6,
    classes=[class_ids['motorcyclist']]
) 

for result in results:
    breakpoint()
    annotated = result.plot()
    cv2.imshow("Video", annotated)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()


