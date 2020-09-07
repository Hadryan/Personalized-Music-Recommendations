import json
import pandas as pd  # dataframe
import re
from spotify_api import SpotifyAPI


class PandoraSongSet:
    def __init__(self, data_file="data.json"):
        try:
            with open(data_file, 'r', encoding="utf8") as f:
                self.data = json.load(f)
        except EnvironmentError as IO_error:
            print("Something is wrong with the file")

        self.songs = pd.DataFrame()

    def create_master_dataframe(self):
        names, artists, likeds = ([] for i in range(3))
        for station in self.data['stations']:
            names += station['songs']['name']
            artists += station['songs']['artist']
            likeds += station['songs']['liked']

        names = self.clean_names(names)
        artists = self.clean_artists(artists)

        audio_features = self.create_audio_features(names, artists)
        with open('temp.json', 'w', encoding='utf-8') as f1:
            json.dump(audio_features, f1, ensure_ascii=False, indent=1)

        station_songs = list(zip(names, artists, likeds))

    def clean_names(self, names):
        pattern = "(?i)(\s\(feat.*)"
        clean_names = [re.sub(pattern, '', name) for name in names]
        return clean_names

    def clean_artists(self, artists):
        pattern = "(?i)\s+\&\s+"
        clean_names = [re.sub(pattern, ' ', artist) for artist in artists]
        return clean_names

    def create_audio_features(self, track_names, track_artists):
        spotify = SpotifyAPI()
        track_ids = []
        for track_name, track_artist in zip(track_names, track_artists):
            track_id = spotify.get_track_id(track_name, track_artist)
            track_ids.append(track_id)
            print(f"Appended {track_name} with {track_id}")
        return spotify.get_audio_features(track_ids)

    def clean_dataframe(self):
        self.songs = self.songs.drop_duplicates().dropna()
        self.songs = self.songs.sort_values(
            ['liked'], ascending=False)

    def build(self):
        self.create_master_dataframe()
        self.clean_dataframe()
