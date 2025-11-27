from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")  
    model.train(
        data="dataset/data.yaml",
        epochs=50,
        imgsz=640,
        batch=8,
        workers=4,
        patience=15
    )
if __name__ == "__main__":
    main()
