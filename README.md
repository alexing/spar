# Spotify Playlist Automated Randomizer (SPAR)

![img.png](img.png)

GitHub Action that refreshes your destination playlist with a random sample of N songs from a larger pool playlist. Runs every Monday at midnight.

**Flow:** Pool playlist (~700 songs) → random sample of N (default 75) → replaces destination playlist. Keeps your watch sync small while the pool stays the source of truth.

## Required GitHub Secrets

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI`
- `SPOTIFY_POOL_PLAYLIST_ID` — your pool (source) playlist
- `SPOTIFY_PLAYLIST_ID` — destination playlist (e.g. for watch sync)
- `SPOTIFY_REFRESH_TOKEN`
- `EMAIL_HOST_PASSWORD` — Gmail app password for notifications

## Config

- `PLAYLIST_SIZE` — number of songs to sync (default: 75). Set in the workflow env or as a secret.
