from ultralytics import YOLO

model = YOLO("yolov8s.pt")


#model.train(data="data.yaml",epochs=50,images=)

#metrics = model.val()
#print(metrics)

#result = model("IMG_0536.JPG", show=True)
#result = model(0,show=True)
#result = model("video.mp4",show=True)
for result in model.track(0,show=True,save=True):
       pass 