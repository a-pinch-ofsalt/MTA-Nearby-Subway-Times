import json
from urllib.parse import parse_qs
from .nearby_times import get_nearest_station_trains

def handler(event, context):
    """
    Vercel-compatible handler for the subway times API.
    Accepts GET requests with required query parameters: latitude and longitude.
    Optional: num_stations (default: 10).
    """
    try:
        # Parse query parameters
        query = parse_qs(event["queryStringParameters"] or {})
        lat = query.get("latitude")
        lon = query.get("longitude")

        # Validate required parameters
        if not lat or not lon:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Missing required query parameters: latitude and longitude"
                })
            }

        # Convert to appropriate types
        lat = float(lat[0])
        lon = float(lon[0])
        num_stations = int(query.get("num_stations", [10])[0])  # Default: 10 stations

        # File path for the station data
        stations_file = "mta-subway-stations-stops.json"

        # Fetch nearest station times
        result = get_nearest_station_trains(lat, lon, stations_file, num_stations)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
