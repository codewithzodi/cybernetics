import cv2
#import numpy as np
import platform
from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient

# Sound alert setup
if platform.system() == "Windows":
    import winsound
    def beep():
        winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms
else:
    import beepy
    def beep():
        beepy.beep(sound="ping")  # Play a beep sound on Linux/macOS

# Load YOLOv8 model for person detection
model_person = YOLO("yolov8s.pt")  # COCO dataset (for people detection)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Overcrowding threshold
OVERCROWDING_THRESHOLD = 2

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        break

    # Convert frame to RGB for YOLO
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run YOLO detections for people
    results_person = model_person(frame_rgb)  # Detect people

    # Count people
    person_count = sum(1 for r in results_person for box in r.boxes if model_person.names[int(box.cls[0])] == "person")

    # Beep if overcrowding detected
    if person_count > OVERCROWDING_THRESHOLD:
        beep()

    # Draw bounding boxes
    for r in results_person:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            cls = int(box.cls[0])
            label = model_person.names[cls]  

            if label == "person":
                color = (0, 255, 0)  # Green for people
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display frame
    cv2.imshow("Surveillance AI", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()