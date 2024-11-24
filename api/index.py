from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs
from .nearby_times import get_nearest_station_trains

from urllib.parse import parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the raw query string
        print(f"DEBUG: Raw path - {self.path}")

        # Parse query parameters
        query = parse_qs(self.path.split("?")[1]) if "?" in self.path else {}
        print(f"DEBUG: Parsed query - {query}")

        lat = query.get("latitude")
        lon = query.get("longitude")
        num_stations = query.get("num_stations", ["10"])

        if not lat:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Missing required query parameter: latitude"
            }).encode())
            return

        try:
            # Convert to appropriate types
            lat = float(lat[0])
            lon = float(lon[0])
            num_stations = int(num_stations[0])

            # File path for the station data
            stations_file = "api/mta-subway-stations-stops.json"

            # Fetch nearest station times
            result = get_nearest_station_trains(lat, lon, stations_file, num_stations)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
