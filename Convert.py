import json
import os
def convert(gps_file):
    with open("pothole_counts.json", "r") as f:
        counts = json.load(f)

    image_list = sorted(counts.keys())
    pothole_counts = [counts[img] for img in image_list]

    gps_coords = []
    with open(gps_file, "r") as f:
        for line in f:
            lat, lon = map(float, line.strip().split(","))
            lat = f"{lat:.6f}"
            lon = f"{lon:.6f}"
            gps_coords.append((lat, lon))

    def get_color(count):
        if count > 5:
            return "red"
        elif count >= 3:
            return "yellow"
        elif count >= 1:
            return "green"
        else:
            return "blue"

    new_gps_color = {}
    for i in range(min(len(pothole_counts), len(gps_coords))):
        lat, lon = gps_coords[i]
        new_gps_color[f"{lat},{lon}"] = get_color(pothole_counts[i])
    if os.path.exists("gps_color.json"):
        with open("gps_color.json", "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}
        existing_data.update(new_gps_color)
        merged_data = existing_data
    else:
        merged_data = new_gps_color

    with open("gps_color.json", "w") as f:
        json.dump(merged_data, f, indent=4)
    print("✅ GPS-color JSON merged and saved as 'gps_color.json'")
