import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get variables from environment
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

def refresh_access_token(client_id, client_secret, refresh_token):
    """Refreshes the Spotify access token using the refresh token."""
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code != 200:
        print("Failed to refresh access token:", response.text)
        return None

    token_info = response.json()
    return token_info.get("access_token")

def get_top_tracks(access_token, limit=50, time_range="long_term"):
    """Fetches the user's top tracks from Spotify."""
    url = f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch top tracks:", response.text)
        return None

    return response.json()

def main():
    # Step 1: Refresh the access token
    access_token = refresh_access_token(client_id, client_secret, refresh_token)
    if not access_token:
        print("Could not refresh access token. Exiting.")
        return

    # Step 2: Fetch top tracks
    data = get_top_tracks(access_token)

    if data and 'items' in data:
        print("\nYour Top Tracks:\n")
        for idx, item in enumerate(data['items']):
            print(f"{idx+1}: {item['name']} by {item['artists'][0]['name']}")
    else:
        print("No top tracks found or error occurred.")

if __name__ == "__main__":
    main()
