import json
from nearest_stations import get_closest_stations, load_stations
from stop_times import get_train_info

def get_nearest_station_trains(lat, lon, stations_file, num_stations=10):
    """
    Get train times for the nearest subway stations as a list of dictionaries.
    Each station is represented as a dictionary with a single key-value pair,
    where the key is the station name, and the value is the train info formatted per route ID.
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
        stop_ids = [f"{stop['stop']}N" for stop in station['stops']] + [f"{stop['stop']}S" for stop in station['stops']]
        all_stop_ids.extend(stop_ids)

    print(f"DEBUG: All stop IDs: {all_stop_ids}")
    print("DEBUG: Fetching train info for all stops...")
    train_info = get_train_info(all_stop_ids)
    print(f"DEBUG: Full train info fetched.")

    # Process train info for each station
    result = []
    for entry in nearest_stations:
        station_index = entry['index']
        station = stations[station_index]
        stop_ids = [f"{stop['stop']}N" for stop in station['stops']] + [f"{stop['stop']}S" for stop in station['stops']]

        # Compact train info for this station
        station_trains = {}
        for stop_id in stop_ids:
            if stop_id in train_info:
                for train in train_info[stop_id]:
                    route_id = train['route_id']
                    headsign = train['headsign']
                    eta = int(train['eta'].split(' ')[0])  # Convert "5 min" to integer 5

                    if route_id not in station_trains:
                        station_trains[route_id] = {}
                    if headsign not in station_trains[route_id]:
                        station_trains[route_id][headsign] = []
                    station_trains[route_id][headsign].append(eta)

        # Add station to result as a dictionary with a single key-value pair
        result.append({station['name']: station_trains})
        print(f"DEBUG: Train info for {station['name']}: {station_trains}")

    return result

if __name__ == "__main__":
    user_latitude = 40.79036810379614
    user_longitude = -73.95362315803276
    stations_file = "mta-subway-stations-stops.json"

    print("DEBUG: Starting main script...")
    train_times = get_nearest_station_trains(user_latitude, user_longitude, stations_file)
    print(json.dumps(train_times, separators=(',', ':')))  # Compact JSON
    print("DEBUG: Script execution completed.")
