import base64
import json
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

# ==== FILL IN YOUR APP CREDENTIALS ====
CLIENT_ID = "7bd99c21e7e74870b5ac2714077c82b2"
CLIENT_SECRET = "25cd31cf9bbd4730be511cc91378673c"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-top-read user-read-recently-played"

# ==== BUILD AUTH URL ====
auth_url = (
    "https://accounts.spotify.com/authorize"
    f"?client_id={CLIENT_ID}"
    "&response_type=code"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope={SCOPE.replace(' ', '%20')}"
)

# ==== SERVER TO CATCH CALLBACK ====
class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "/callback" in self.path:
            code = self.path.split("code=")[-1]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>You can close this window now!</h1>")
            self.server.auth_code = code

def start_server():
    server = HTTPServer(('localhost', 8888), SpotifyAuthHandler)
    server.handle_request()
    return server.auth_code

# ==== MAIN FLOW ====
def main():
    print("Opening browser for Spotify authorization...")
    webbrowser.open(auth_url)

    auth_code = start_server()
    print(f"Authorization code: {auth_code}")

    # ==== EXCHANGE CODE FOR TOKEN ====
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)
    token_info = response.json()

    print("\nAccess Token:")
    print(token_info.get("access_token"))
    print("\nRefresh Token:")
    print(token_info.get("refresh_token"))
    print("\nExpires In (seconds):")
    print(token_info.get("expires_in"))

if __name__ == "__main__":
    main()
