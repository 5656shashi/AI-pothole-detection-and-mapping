import folium
import json
def map1():
    with open("gps_color.json") as f:
        data = json.load(f)
    if not data:
        folium.Map(location=[12.9716, 77.5946], zoom_start=13).save("generated/pothole_map.html")
        return
    first = list(data.keys())[0].split(",")
    m = folium.Map(location=[float(first[0]), float(first[1])], zoom_start=15)
    for gps, status in data.items():
        lat, lon = map(float, gps.split(","))
        color = "red" if status=="red" else (
                "orange" if status=="yellow" else (
                "green" if status=="green" else("blue")
                )
        )
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    m.save("generated\pothole_map.html")
    print("Map saved as pothole_map.html")
    return
map1()