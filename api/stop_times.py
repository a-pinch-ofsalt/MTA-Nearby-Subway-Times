from nyct_gtfs import NYCTFeed
from datetime import datetime

def get_train_info(stop_ids):
    """
    Get train arrival information for a list of stop IDs.
    """
    feeds = [
        NYCTFeed("A"),
        NYCTFeed("G"),
        NYCTFeed("N"),
        NYCTFeed("1"),
        NYCTFeed("B"),
        NYCTFeed("J"),
        NYCTFeed("L"),
        NYCTFeed("SIR")
    ]

    trains_heading_to_stops = {stop_id: [] for stop_id in stop_ids}
    print(f"DEBUG: Initialized train info for {len(stop_ids)} stops.")

    for feed in feeds:
        print(f"DEBUG: Processing feed for {str(feed)}...")
        for stop_id in stop_ids:
            for train in feed.filter_trips(headed_for_stop_id=[stop_id]):
                for update in train.stop_time_updates:
                    if update.stop_id == stop_id and update.arrival is not None:
                        eta_minutes = (update.arrival - datetime.now()).total_seconds() // 60
                        if eta_minutes > 0:
                            trains_heading_to_stops[stop_id].append({
                                'route_id': train.route_id,
                                'headsign': train.headsign_text,
                                'eta': f"{int(eta_minutes)} min"
                            })
        print(f"DEBUG: Completed processing for feed {str(feed)}.")
    print("DEBUG: Train info retrieval complete.")
    return trains_heading_to_stops