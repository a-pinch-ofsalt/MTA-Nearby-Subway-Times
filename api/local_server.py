from flask import Flask, request, jsonify
from nearby_times import get_nearest_station_trains

app = Flask(__name__)

@app.route('/api/subway_times', methods=['GET'])
def subway_times():
    # Parse query parameters
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    num_stations = request.args.get('num_stations', 10)

    # Validate required parameters
    if not lat or not lon:
        return jsonify({
            "error": "Missing required query parameters: latitude and longitude"
        }), 400

    try:
        # Convert to appropriate types
        lat = float(lat)
        lon = float(lon)
        num_stations = int(num_stations)

        # File path for the station data
        stations_file = "mta-subway-stations-stops.json"

        # Fetch nearest station times
        result = get_nearest_station_trains(lat, lon, stations_file, num_stations)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
