from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import cv2
import detect2,Convert,Map
import shutil
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generated/<path:filename>')
def generated_map(filename):
    return send_from_directory('generated', filename)

@app.route('/login_admin', methods=['POST'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "admin" and password == "password":
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/generate', methods=['POST'])
def generate():
    video_path = request.form.get('video')
    gps_path = request.form.get('gps')
    output_folder = r"dataset\new\images"
    os.makedirs(output_folder, exist_ok=True)
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)   
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  
        frame_count += 1
        frame_filename = f"frame_{frame_count:04d}.jpg"
        cv2.imwrite(os.path.join(output_folder, frame_filename), frame)
        print(f"Saved: {frame_filename}")
    cap.release()
    print(f"\n✅ Done! Total frames saved: {frame_count}")
    detect2.getpotholeinfo()
    Convert.convert(gps_path)
    Map.map1()
    generated_map("pothole_map.html")
    return jsonify({"success": True})

@app.route('/delete', methods=['POST'])
def delete_gps():
    gps_path = request.form.get("gps_file")  
    if not gps_path or not os.path.exists(gps_path):
        return jsonify({"success": False, "error": "GPS file not found"})
    with open("gps_color.json", "r") as f:
        data = json.load(f)
    if not data:
        return jsonify({"success": True, "removed": 0  })
    with open(gps_path, "r") as f:
        gps_to_remove = set(line.strip() for line in f)
    print(gps_to_remove)
    filtered_data = {k: v for k, v in data.items() if k not in gps_to_remove}
    print(filtered_data)
    with open("gps_color.json", "w") as f:
        json.dump(filtered_data, f, indent=4)
    Map.map1()
    generated_map("pothole_map.html")
    return jsonify({"success": True, "removed": len(data) - len(filtered_data)})
if __name__ == '__main__':
    app.run(debug=True)
