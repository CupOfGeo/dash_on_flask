from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_client_id"],
                                               client_secret=os.environ['SPOTIFY_client_secret'],))


def get_playlist_name(playlist_id):
    pl_id = f'spotify:playlist:{playlist_id}'
    results = sp.playlist(pl_id)
    playlist_name = results['name']
    return playlist_name