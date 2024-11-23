import json
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points on the Earth.
    """
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def load_stations(file_path):
    """
    Load subway station data from a JSON file.
    """
    print("DEBUG: Opening station data file...")
    with open(file_path, 'r') as f:
        data = json.load(f)
    print("DEBUG: Station data loaded.")
    return data

def get_closest_stations(lat, lon, stations, num_results=10):
    """
    Get the closest subway stations to the provided coordinates.
    """
    print("DEBUG: Calculating distances to all stations...")
    closest_stations = []

    for index, station in enumerate(stations):
        if index % 10 == 0:
            print(f"DEBUG: Processed {index}/{len(stations)} stations...")

        stops = station['stops']
        closest_stop = min(
            stops, key=lambda stop: haversine_distance(lat, lon, stop['latitude'], stop['longitude'])
        )
        distance = haversine_distance(lat, lon, closest_stop['latitude'], closest_stop['longitude'])
        closest_stations.append({"index": index, "distance": distance})

    print("DEBUG: Sorting stations by distance...")
    closest_stations.sort(key=lambda x: x['distance'])
    print("DEBUG: Sorting complete.")
    return closest_stations[:num_results]

if __name__ == "__main__":
    user_latitude = 40.7580
    user_longitude = -73.9855
    station_file = "mta-subway-stations-stops.json"

    print("DEBUG: Running nearest stations script...")
    stations = load_stations(station_file)
    nearest_stations = get_closest_stations(user_latitude, user_longitude, stations)
    print(json.dumps(nearest_stations, indent=2))
