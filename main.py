from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

from emails import send_email
from shuffle import shuffle_n_times

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
playlist_id = os.getenv('SPOTIFY_PLAYLIST_ID')
chunk_size = 100


def create_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
        scope='playlist-modify-public playlist-modify-private playlist-read-private',
        cache_path=None  # Disable cache_path in CI environment
    ))

    return sp


def refresh_spotify_token(sp):
    token_info = sp.auth_manager.get_cached_token()

    if sp.auth_manager.is_token_expired(token_info):
        print("Refreshing token")
        token_info = sp.auth_manager.refresh_access_token(token_info['refresh_token'])
        sp.auth_manager.token_info = token_info
    else:
        print("Token valid")

    return sp


def main():
    sp = create_spotify_client()
    sp = refresh_spotify_token(sp)

    playlist_name = sp.playlist(playlist_id).get("name")
    user_id = sp.me()['id']
    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"

    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    track_ids = [track['track']['id'] for track in tracks]
    print(f"Got all tracks from {playlist_name}: {len(track_ids)} tracks.")

    backup_playlist_name = f"dale-bkp-{datetime.now().isoformat()}"
    backup_playlist = sp.user_playlist_create(user_id, backup_playlist_name, public=False,
                                              description='Backup playlist')
    backup_playlist_id = backup_playlist.get("id")
    for i in range(0, len(track_ids), chunk_size):
        sp.playlist_add_items(backup_playlist_id, track_ids[i:i + chunk_size])
    backup_playlist_url = f"https://open.spotify.com/playlist/{backup_playlist_id}"
    print(f"Created backup: {backup_playlist_name} @ {backup_playlist_url}")

    shuffled_ids = shuffle_n_times(track_ids.copy(), 5)
    sp.playlist_replace_items(playlist_id, [])
    for i in range(0, len(shuffled_ids), chunk_size):
        sp.playlist_add_items(playlist_id, shuffled_ids[i:i + chunk_size])
    print(f"shuffle done ✨")

    send_email(subject='Dale shuffled successfully!', body=f"""
    Succesfully shuffled {playlist_name}: {playlist_url}
    backup now is {backup_playlist_name}: {backup_playlist_url}
    """)
    print("bye!👋🏻")


if __name__ == "__main__":
    main()
