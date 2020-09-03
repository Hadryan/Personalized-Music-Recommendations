import json
import pandas as pd  # dataframe
import requests  # for making HTTP requests


class PandoraSongSet:
    def __init__(self, data_file="data.json"):
        with open(data_file, 'r', encoding="utf8") as f:
            self.data = json.load(f)

    def create_master_list(self):
