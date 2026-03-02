from ultralytics import YOLO
import cv2
import beepy  # Library for beep sounds

# Load the YOLOv8m model
model = YOLO("yolov8m.pt")  

# Define the target classes
TARGET_CLASSES = ["knife", "gun", "helmet", "fire", "overcrowd"]  

# Open webcam or video file (change "0" to "video.mp4" for a file)
cap = cv2.VideoCapture(0)  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference
    results = model(frame)

    detected = False  # Flag to track detections

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0].item()  # Confidence score
            cls_id = int(box.cls[0].item())  # Class ID
            class_name = model.names[cls_id]  # Get class label

            # Only process if class is in our target list
            if class_name in TARGET_CLASSES:
                label = f"{class_name}: {conf:.2f}"
                detected = True  # Set flag to True if a target object is found

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Play beep sound if a target object is detected
    if detected:
        beepy.beep(sound=1)  # Beep sound (you can change the sound type)

    # Show result
    cv2.imshow("YOLOv8m Detection with Beep Alert", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
