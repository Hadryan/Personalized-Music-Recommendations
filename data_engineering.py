import json
import pandas as pd  # dataframe
import requests  # for making HTTP requests


class PandoraSongSet:
    def __init__(self, data_file="data.json"):
        try:
            with open(data_file, 'r', encoding="utf8") as f:
                self.data = json.load(f)
        except EnvironmentError as IO_error:
            print("Something is wrong with the file")

        self.songs = pd.DataFrame(columns=[
            'name', 'artist', 'liked'])

    def create_master_dataframe(self):
        for station in self.data['stations']:
            name = station['songs']['name']
            artist = station['songs']['artist']
            liked = station['songs']['liked']
            station_songs = list(zip(name, artist, liked))

            self.songs = self.songs.append(
                pd.DataFrame(station['songs']), ignore_index=True)

    def clean_dataframe(self):
        self.songs = self.songs.drop_duplicates()
        self.songs = self.songs.sort_values(
            ['liked'], ascending=False)

    def append_audio_features(self):
        pass

    def build(self):
        self.create_master_dataframe()
        self.clean_dataframe()
