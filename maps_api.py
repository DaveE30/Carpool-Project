from dotenv import load_dotenv
import os
import googlemaps


load_dotenv()
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
print(f'this is api key: ', google_maps_api_key)
print(f"Google Maps API Key loaded: {google_maps_api_key is not None}")

gmaps = googlemaps.Client(key=google_maps_api_key)

def get_directions(origin, destination):
    try:
        directions_result = gmaps.directions(origin, destination, mode="driving")
        distance = directions_result[0]['legs'][0]['distance']['text']
        duration = directions_result[0]['legs'][0]['duration']['text']  
        print(f"Distance and duration from {origin} to {destination}: \nDistance = {distance}, \nDuration = {duration}")
        return directions_result
    except Exception as e:
        print(f"Error getting directions: {e}")
        return None
    
get_directions("17-29 bleecker st, ridgewood, ny", "17-83 stanhope st, ridgewood, ny")

