from dotenv import load_dotenv
import os
import googlemaps
import json


load_dotenv()
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')


gmaps = googlemaps.Client(key=google_maps_api_key)

def get_directions_and_map(origin, destination, waypoints=[]):
    try:
        directions_result = gmaps.directions(origin, destination, waypoints=waypoints, optimize_waypoints=True, mode="driving")
        distances = []
        durations = []
        leg_info = directions_result[0]['legs']

        leg_strings = []  # collect per-leg strings
        for i, leg in enumerate(leg_info):
            leg_distance = leg['distance']['text']
            distances.append(leg_distance)
            leg_duration = leg['duration']['text']
            durations.append(leg_duration)
            #instead of a string can we store a dict?
            leg_strings.append({
                "leg_number": i+1,
                "start_address": leg['start_address'],
                "end_address": leg['end_address'],
                "distance": leg_distance,
                "duration": leg_duration
            })

        total_distance = sum([float(d.split()[0]) for d in distances])
        total_duration = 0
        for t in durations:
            if "hour" in t.lower():
                # Extract hours and minutes
                parts = t.split()
                hours = 0
                minutes = 0
                for i, part in enumerate(parts):
                    if "hour" in part.lower():
                        hours = int(parts[i-1])
                    elif "min" in part.lower():
                        minutes = int(parts[i-1])
                total_duration += (hours * 60) + minutes
            else:
                # Only minutes
                minutes = int(t.split()[0])
                total_duration += minutes

        polyline = directions_result[0]['overview_polyline']['points']
        map_result = gmaps.static_map(
            size=(600, 400),
            zoom=11,
            format="png",
            maptype="roadmap",
            center=origin,
            markers=[origin, destination] + waypoints,
            path=f"color:0x0000ff|weight:5|enc:{polyline}"
        )
        with open("static/map.png", "wb") as f:
            for chunk in map_result:
                f.write(chunk)
        print("Map image saved as static/map.png")

        return leg_strings, total_distance, total_duration, "map.png", distances, durations
    except Exception as e:
        print(f"Error getting directions: {e}")
        return (None, None, None, None, None, None)
    
# get_directions_and_map("cuny york college", "union square, new york, ny", ["queens center mall", "jkf airport", "pink forest cafe, forest hills, ny"])

# def get_map(origin, destination, waypoints=[]):
#     try:
#         map_result = gmaps.static_map(size=(600,400), zoom=13, format="png",maptype="roadmap", markers=[origin, destination] + waypoints, path="color:0x0000ff|weight:5|geodesic:True" + "|".join([origin] + waypoints + [destination]))
#         with open("map.png", "wb") as f:
#             for chunk in map_result:
#                 f.write(chunk)
#         print("Map image saved as map.png")
#         return "map.png"
#     except Exception as e:
#         print(f"Error getting map: {e}")
#         return None

# get_map("17-29 bleecker st, ridgewood, ny", "17-83 stanhope st, ridgewood, ny", ["queens center mall", "forest hills, ny", "pink forest cafe, forest hills, ny"])

