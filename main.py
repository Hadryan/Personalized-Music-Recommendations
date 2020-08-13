# Standard library
import json
import time
# Related third party
from bs4 import BeautifulSoup # html/xml parser
import pandas as pd # dataframe
import requests # grab webpages
from selenium import webdriver # affect javascript actions easily
from selenium.webdriver.common.keys import Keys # common key commands

# Load json credentials
with open("config.json",'r') as f:
  config = json.load(f)

# Web scrape songs from Pandora with liked or not liked attribute
DRIVER_PATH = "assets\\chromedriver.exe"
driver = webdriver.Chrome(DRIVER_PATH)
driver.implicitly_wait()

driver.get("https://www.pandora.com/account/sign-in")
driver.find_element_by_name('username').send_keys(config['pandora']['username'])
driver.find_element_by_name('password').send_keys(config['pandora']['password'])
driver.find_element_by_css_selector("button[data-qa='login_button']").click()


# Create dataframe of Pandora songs with Spotify audio features

# Create model based on features

# Adjust models via balancing and different estimators

# Find new recommendations
## Randomly select songs from the Spotify database
## Use graph network to find songs of similiar users
## Use songs similiar in features