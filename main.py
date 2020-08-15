# Standard library
import time

# Related third party
from bs4 import BeautifulSoup # html/xml parser
import pandas as pd # dataframe
import requests # for making HTTP requests

# Local application
import webscraper
from webscraper import WebScraper

### Web scrape songs from Pandora with liked or not liked attribute

### Create dataframe of Pandora songs with Spotify audio features

### Create model based on features

### Adjust models via balancing and different estimators

### Find new recommendations
## Randomly select songs from the Spotify database
## Use graph network to find songs of similiar users
## Use songs similiar in features

def main():
  webscraper = WebScraper(is_headless=False)
  webscraper.login()
  time.sleep(6)
  webscraper.get_stations()
  input('Press ENTER to exit browser')
  webscraper.logout()
  time.sleep(2)
  webscraper.close_browser()
  input('Press ENTER to exit program')

if __name__ == "__main__":
    main()
