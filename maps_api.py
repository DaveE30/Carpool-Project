from dotenv import load_dotenv
import os
import googlemaps
import json


load_dotenv()
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
print(f'this is api key: ', google_maps_api_key)
print(f"Google Maps API Key loaded: {google_maps_api_key is not None}")

gmaps = googlemaps.Client(key=google_maps_api_key)

def get_directions_and_map(origin, destination, waypoints=[]):
    try:
        directions_result = gmaps.directions(origin, destination, waypoints=waypoints, optimize_waypoints=False, mode="driving")
        # print("DIRECTIONS RESULT:", directions_result)
        # get distance and duration for each leg of the trip    
        total_distance = []
        total_duration = []
        for i, leg in enumerate(directions_result[0]['legs']):
            leg_distance = leg['distance']['text']
            total_distance.append(leg_distance)
            leg_duration = leg['duration']['text']
            total_duration.append(leg_duration)
            leg_info=(f"Leg {i+1} starting from {leg['start_address']} to {leg['end_address']}: Distance = {leg_distance}, Duration = {leg_duration}")
            print(leg_info)
        #sum the total distances and durations
        total_distance = sum([float(d.split()[0]) for d in total_distance])
        total_duration = sum([int(t.split()[0]) for t in total_duration])
        print("Total Distances for trip:", total_distance)
        print("Total Durations for trip:", total_duration)
        polyline = directions_result[0]['overview_polyline']['points']
        map_result = gmaps.static_map(size=(600,400), zoom=11, format="png",maptype="roadmap",center=origin, markers=[origin, destination] + waypoints, path=f"color:0x0000ff|weight:5|enc:{polyline}")
        with open("map.png", "wb") as f:
            for chunk in map_result:
                f.write(chunk)
        print("Map image saved as map.png")
       
        
        return leg_info, total_distance, total_duration, "map.png"
    except Exception as e:
        print(f"Error getting directions: {e}")
        return None
    
get_directions_and_map("cuny york college", "union square, new york, ny", ["queens center mall", "jkf airport", "pink forest cafe, forest hills, ny"])

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

