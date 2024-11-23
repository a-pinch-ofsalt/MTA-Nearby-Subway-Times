import json
from nearest_stations import get_closest_stations, load_stations
from stop_times import get_train_info

def get_nearest_station_trains(lat, lon, stations_file, num_stations=10):
    """
    Get train times for the nearest subway stations as a list of dictionaries.
    """
    print("DEBUG: Loading station data...")
    stations = load_stations(stations_file)
    print(f"DEBUG: Loaded {len(stations)} stations.")

    print("DEBUG: Finding closest stations...")
    nearest_stations = get_closest_stations(lat, lon, stations, num_stations)
    print(f"DEBUG: Found {len(nearest_stations)} closest stations.")

    # Gather all stop IDs for nearest stations
    all_stop_ids = []
    for entry in nearest_stations:
        station_index = entry['index']
        station = stations[station_index]
        print(f"DEBUG: Gathering stop IDs for station: {station['name']}")

        for stop in station['stops']:
            all_stop_ids.extend([f"{stop['stop']}N", f"{stop['stop']}S"])

    print(f"DEBUG: Fetching train info for {len(all_stop_ids)} stop IDs...")
    train_info = get_train_info(all_stop_ids)

    # Assign train times back to stations
    result = []
    for entry in nearest_stations:
        station_index = entry['index']
        station = stations[station_index]
        stop_ids = [
            f"{stop['stop']}N" for stop in station['stops']
        ] + [f"{stop['stop']}S" for stop in station['stops']]

        station_entry = {
            "name": station['name'],
            "trains": []
        }
        for stop_id in stop_ids:
            station_entry["trains"].extend(train_info.get(stop_id, []))
        
        result.append(station_entry)

    return result

if __name__ == "__main__":
    user_latitude = 40.79036810379614
    user_longitude = -73.95362315803276
    stations_file = "mta-subway-stations-stops.json"

    print("DEBUG: Starting main script...")
    train_times = get_nearest_station_trains(user_latitude, user_longitude, stations_file)
    print(json.dumps(train_times, indent=2))
    print("DEBUG: Script execution completed.")
