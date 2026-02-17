import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

if not client_id or not client_secret:
    size = env_path.stat().st_size if env_path.exists() else 0
    print(f"Error: Could not load SPOTIFY_CLIENT_ID/SECRET from .env")
    print(f"  Path: {env_path}")
    print(f"  File size: {size} bytes")
    if size == 0:
        print("  → .env is empty. Add your credentials and save the file.")
    sys.exit(1)

auth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-modify-public playlist-modify-private playlist-read-private",
)

# Opens browser → log in → authorize
token = auth.get_access_token(as_dict=True)
print("\n--- COPY THIS ---")
print("SPOTIFY_REFRESH_TOKEN=" + token["refresh_token"])
print("--- END ---\n")