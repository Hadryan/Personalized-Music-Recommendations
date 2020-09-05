import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAPI:
    def __init__(self):
        self.authenticate()

    def authenticate(self, credentials_file="credentias.json"):
        try:
            with open(credentials_file, 'r', encoding="utf8") as f:
                credentials = json.load(f)
            client_id = credentials['spotify']['id']
            client_secret = credentials['spotify']['secret']

            client_credentials_manager = SpotifyClientCredentials(
                client_id, client_secret)
            sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)
            print("Spotify authentication successful")
        except EnvironmentError as io_error:
            print(io_error)
