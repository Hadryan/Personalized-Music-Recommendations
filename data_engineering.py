import json
import pandas as pd
import re
from spotify_api import SpotifyAPI


class PandoraSongSet:
    def __init__(self, data_file=r"inputs\data.json"):
        try:
            with open(data_file, 'r', encoding="utf8") as f:
                self.data = json.load(f)
        except EnvironmentError as IO_error:
            print("Something is wrong with the data file.")

        self.songs = pd.DataFrame()

    def create_master_dataframe(self):
        names, artists, likeds = ([] for i in range(3))
        for station in self.data['stations']:
            names += station['songs']['name']
            artists += station['songs']['artist']
            likeds += station['songs']['liked']

        names = self.clean_names(names)
        artists = self.clean_artists(artists)

        station_songs = list(
            zip(names, artists, likeds))
        station_songs_df = pd.DataFrame(
            station_songs, columns=['name', 'artist', 'liked'])

        audio_features = self.create_audio_features(names, artists)
        default_values = {'danceability': None, 'energy': None, 'key': None, 'loudness': None, 'mode': None, 'speechiness': None, 'acousticness': None, 'instrumentalness': None,
                          'liveness': None, 'valence': None, 'tempo': None, 'type': None, 'id': None, 'uri': None, 'track_href': None, 'analysis_url': None, 'duration_ms': None, 'time_signature': None}
        audio_features = [default_values if features ==
                          None else features for features in audio_features]
        audio_features_df = pd.DataFrame(audio_features)

        self.unclean_songs = pd.concat(
            [station_songs_df, audio_features_df], axis=1)

        try:
            self.unclean_songs.to_csv(r"outputs\unclean_songs.csv")
            print("The full songs CSV has been made.")
        except Exception as e:
            print(
                f"Something is wrong with the creation of the full songs dataframe file.")
            print(e)

    def clean_names(self, names):
        pattern1 = "^(\s)"
        pattern2 = "(?i)(\s\(feat.*)"
        pattern3 = "(?i)(\sEdit.*)"

        clean_names = [re.sub(pattern1, '', name) for name in names]
        clean_names = [re.sub(pattern2, '', name) for name in clean_names]
        clean_names = [re.sub(pattern3, '', name) for name in clean_names]

        return clean_names

    def clean_artists(self, artists):
        pattern1 = "^(\s)"
        pattern2 = "(?i)(\s+\&\s+)"
        clean_artists = [re.sub(pattern1, '', artist) for artist in artists]
        clean_artists = [re.sub(pattern2, ' ', artist)
                         for artist in clean_artists]
        return clean_artists

    def create_audio_features(self, track_names, track_artists):
        spotify = SpotifyAPI()
        track_ids = []
        for track_name, track_artist in zip(track_names, track_artists):
            track_id = spotify.get_track_id(track_name, track_artist)
            track_ids.append(track_id)
            # print(f"Appended {track_name} with {track_id}")
        return spotify.get_audio_features(track_ids)

    def clean_dataframe(self):
        self.songs = self.unclean_songs.drop_duplicates().dropna()
        self.songs = self.songs.sort_values(
            ['liked'], ascending=False)
        try:
            self.songs.to_csv(r"outputs\songs.csv")
            print("The cleaned songs CSV has been made.")
        except Exception as e:
            print(
                "Something is wrong with the creation of the cleaned songs dataframe file.")
            print(e)

    def build(self):
        self.create_master_dataframe()
        self.clean_dataframe()
