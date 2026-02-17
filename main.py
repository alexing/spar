import os
from pathlib import Path

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from emails import send_email

load_dotenv(Path(__file__).resolve().parent / ".env")
from shuffle import sample_n

CHUNK_SIZE = 100

pool_playlist_id = os.getenv('SPOTIFY_POOL_PLAYLIST_ID')
destination_playlist_id = os.getenv('SPOTIFY_PLAYLIST_ID')
playlist_size = int(os.getenv('PLAYLIST_SIZE', '75'))


def create_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
        scope='playlist-modify-public playlist-modify-private playlist-read-private',
        cache_path=None,
    )
    token_info = auth_manager.refresh_access_token(os.getenv("SPOTIFY_REFRESH_TOKEN"))
    access_token = token_info["access_token"]

    sp = spotipy.Spotify(auth=access_token)
    return sp, auth_manager


def refresh_spotify_token(auth_manager):
    token_info = auth_manager.get_access_token(as_dict=False)
    if not auth_manager.validate_token(token_info):
        print("Refreshing token")
        auth_manager.refresh_access_token(os.getenv('SPOTIFY_REFRESH_TOKEN'))
    else:
        print("Token valid")


def fetch_all_track_ids(sp, playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [track['track']['id'] for track in tracks if track['track']]


def main():
    sp, auth_manager = create_spotify_client()
    refresh_spotify_token(auth_manager)

    pool_playlist = sp.playlist(pool_playlist_id)
    pool_name = pool_playlist['name']
    pool_url = f"https://open.spotify.com/playlist/{pool_playlist_id}"

    dest_playlist = sp.playlist(destination_playlist_id)
    dest_name = dest_playlist['name']
    dest_url = f"https://open.spotify.com/playlist/{destination_playlist_id}"

    track_ids = fetch_all_track_ids(sp, pool_playlist_id)
    print(f"Pool '{pool_name}': {len(track_ids)} tracks.")

    if not track_ids:
        send_email(
            subject='SPAR: Pool is empty',
            body=f"Pool playlist is empty. Nothing to sync.\n{pool_url}"
        )
        print("Pool empty, exiting.")
        return

    sampled_ids = sample_n(track_ids, playlist_size)
    n_used = len(sampled_ids)
    if n_used < playlist_size:
        print(f"Pool has fewer than {playlist_size} songs, using all {n_used}.")

    sp.playlist_replace_items(destination_playlist_id, [])
    for i in range(0, len(sampled_ids), CHUNK_SIZE):
        sp.playlist_add_items(destination_playlist_id, sampled_ids[i:i + CHUNK_SIZE])
    print(f"Synced {n_used} songs to '{dest_name}' ✨")

    send_email(
        subject='SPAR: Playlist refreshed',
        body=f"""
Refreshed {dest_name} with {n_used} random songs from your pool.

Destination: {dest_url}
Pool: {pool_url}
"""
    )
    print("bye!👋🏻")


if __name__ == "__main__":
    main()
