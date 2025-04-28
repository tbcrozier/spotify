import os
import requests
import json
from google.cloud import pubsub_v1
from datetime import datetime

# Setup Pub/Sub publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('GCP_PROJECT'), os.getenv('PUBSUB_TOPIC'))

# Spotify API Access Token (provided via environment variable)
SPOTIFY_ACCESS_TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN')

def main(request):
    """Polls Spotify recently played tracks and publishes to Pub/Sub."""
    headers = {
        "Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"
    }

    # Call Spotify API
    response = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?limit=5",
        headers=headers
    )

    if response.status_code != 200:
        return f"Spotify API error: {response.text}", 500

    data = response.json()

    for item in data.get('items', []):
        played_at = item['played_at']
        track = item['track']['name']
        artist = item['track']['artists'][0]['name']
        ms_played = item.get('ms_played', None)

        event = {
            "ts": played_at,
            "track": track,
            "artist": artist,
            "ms_played": ms_played,
            "raw_event": json.dumps(item)  # Save full original Spotify event
        }

        # Publish event to Pub/Sub
        publisher.publish(
            topic_path,
            data=json.dumps(event).encode("utf-8")
        )

    return "Successfully published Spotify events to Pub/Sub!", 200
