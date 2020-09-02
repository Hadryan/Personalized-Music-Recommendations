# Standard library
import time

# Related third party
from bs4 import BeautifulSoup  # html/xml parser
import pandas as pd  # dataframe
import requests  # for making HTTP requests

# Local application
from webscraper import WebScraper

# Web scrape songs from Pandora with liked or not liked attribute


def activate_webscraper():
    webscraper = WebScraper(is_headless=True)
    webscraper.login()
    station_URLs = webscraper.get_stations_URLs()
    webscraper.get_songs(station_URLs)
    # webscraper.get_songs(["https://www.pandora.com/station/34242"])
    # webscraper.get_songs(["https://www.pandora.com/station/34242",
    #                       "https://www.pandora.com/station/4550091192589184342", "https://www.pandora.com/station/3852655062826970454"])
    input('Press ENTER to exit browser')
    webscraper.close_browser()

# Create dataframe of Pandora songs with Spotify audio features

# Create model based on features

# Adjust models via balancing and different estimators

# Find new recommendations
# Randomly select songs from the Spotify database
# Use graph network to find songs of similiar users
# Use songs similiar in features


def main():
    activate_webscraper()


if __name__ == "__main__":
    main()
