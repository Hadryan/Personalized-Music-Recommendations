import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAPI:
    def __init__(self):
        self.authenticate()

    def authenticate(self, credentials_file="credentials.json"):
        try:
            with open(credentials_file, 'r', encoding="utf8") as f:
                credentials = json.load(f)
            client_id = credentials['spotify']['id']
            client_secret = credentials['spotify']['secret']

            client_credentials_manager = SpotifyClientCredentials(
                client_id, client_secret)
            self.sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)
            print("Spotify authentication successful")
        except EnvironmentError as io_error:
            print(io_error)

    def track_exists(self, track):
        track_json = self.sp.search(track, limit=1)
        test = track_json['tracks']['total']
        return True if test > 0 else False

    def get_track_id(self, track):
        try:
            track_json = self.sp.search(track, limit=1)
            track_id = track_json['tracks']['items'][0]['id']
            return track_id
        except Exception as e:
            print(e)
            return "NaN"
