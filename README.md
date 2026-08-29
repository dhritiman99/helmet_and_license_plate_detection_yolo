Helmet and License Plate Detection (YOLO)

A computer vision pipeline built with YOLO to detect motorcycle riders, verify helmet usage, and locate license plates in real time. 

This project is aimed at automated traffic monitoring systems to help identify safety violations, specifically targeting unhelmeted riders and reading their license plates.

---

## ✨ Features

- **Multi-Object Detection:** Tracks riders, helmets, missing helmets, and license plates in a single pass.
- **Real-Time Performance:** Optimized for fast inference on images, video feeds, and live webcam streams.
- **Violation Tracking:** Designed to isolate and crop license plates when a helmet violation is flagged.

---

## 📁 Repository Layout

```text
helmet_and_license_plate_detection_yolo/
├── dataset/       # Raw and processed dataset files
├── models/        # Trained model weights (.pt)
├── inference/     # Output detections (images/videos)
├── notebooks/     # Jupyter notebooks for training & testing
├── utils/         # Data prep and bounding box helpers
├── main.py        # Detection script
└── requirements.txt
```

---

## 🛠️ Quickstart

### 1. Clone & Set Up

```bash
git clone https://github.com/dhritiman99/helmet_and_license_plate_detection_yolo.git
cd helmet_and_license_plate_detection_yolo
```

It is recommended to use a virtual environment:

```bash
# Using Conda
conda create -n helmet-yolo python=3.9 -y
conda activate helmet-yolo

# Install dependencies
pip install -r requirements.txt
```

---

## 🏃 Running Detections

**On a single image:**
```bash
python main.py --source path/to/image.jpg --weights models/best.pt --conf 0.4
```

**On a video file or live stream:**
```bash
python main.py --source path/to/video.mp4 --weights models/best.pt --conf 0.5 --save-vid
```

---

## 🏋️ Model Training

To train the detector on your custom dataset using Ultralytics YOLO:

1. Format your images and labels following the YOLO directory format.
2. Update your `data.yaml` paths and class labels.
3. Run the training script:

```python
from ultralytics import YOLO

# Load base model
model = YOLO("yolov8n.pt")

# Start training
model.train(data="data.yaml", epochs=50, imgsz=640, batch=16)
```

---

## 📊 Class Labels

- **Helmet:** Rider wearing standard safety gear.
- **No Helmet:** Rider operating without a helmet (triggers violation handling).
- **License Plate:** Vehicle license plate location for identification.

---

## 🤝 Contributing

Pull requests are always welcome. Feel free to open an issue first if you want to suggest major changes or report bugs.

## 📜 License

[MIT](LICENSE)
