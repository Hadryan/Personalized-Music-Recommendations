import json
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAPI:
    def __init__(self):
        self.__authenticate()

    def __authenticate(self, credentials_file=r"authentication\credentials.json"):
        try:
            with open(credentials_file, 'r', encoding="utf8") as f:
                credentials = json.load(f)
            client_id = credentials['spotify']['id']
            client_secret = credentials['spotify']['secret']

            client_credentials_manager = SpotifyClientCredentials(
                client_id, client_secret)
            self.sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager)
            print("Spotify authentication successful!")
        except EnvironmentError as io_error:
            print(io_error)

    def track_exists(self, track):
        track_json = self.sp.search(track, limit=1)
        test = track_json['tracks']['total']
        return True if test > 0 else False

    def get_track_id(self, track, artist):
        query = track + " " + artist
        while query != '':
            try:
                track_json = self.sp.search(query, limit=1)
                track_id = track_json['tracks']['items'][0]['id']
                return track_id
            except Exception as e:
                return "NaN"
                pd.DataFrame([query]).to_clipboard(
                    excel=False, index=False, header=False)
                query = input(
                    f"The query: [{query}] did not work. Type a new one or press ENTER to fill with NaN.\n")
                if query == '':
                    query = input(f"Are you sure? Press ENTER again.\n")
        return "NaN"

    def get_audio_features(self, tracks):
        n = 100
        track_features = []
        tracks = [tracks[i:i+n] for i in range(0, len(tracks), n)]
        for track_group in tracks:
            track_features += self.sp.audio_features(track_group)
        return track_features
