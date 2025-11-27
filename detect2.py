from ultralytics import YOLO
import cv2
import os
import json

def getpotholeinfo():
    model = YOLO("best.pt")

    input_folder = "dataset/new/images"  
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    json_file = "pothole_counts.json"
    valid_ext = (".jpg", ".jpeg", ".png")
    pothole_counts = {}
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_ext):

            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)
            results = model(img)
            count = 0
            for r in results:
                count += len(r.boxes)  
                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = float(box.conf[0])
                    cv2.rectangle(img,
                                (int(x1), int(y1)),
                                (int(x2), int(y2)),
                                (0, 255, 0), 2)

                    cv2.putText(img, f"Pothole {conf:.2f}",
                                (int(x1), int(y1)-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0,255,0), 2)

            out_path = os.path.join(output_folder, filename)
            cv2.imwrite(out_path, img)
            pothole_counts[filename] = count
            print(f"Processed: {filename}, Potholes: {count}")

    with open(json_file, "w") as f:
        json.dump(pothole_counts, f, indent=4)

    print(f"\n✅ Detection complete! Counts saved in '{json_file}'.")
    return
