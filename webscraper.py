# Standard library
import json
import time
import random

# Related third party
from selenium import webdriver # Launch/initialise a browser and affect javascript easily
from selenium.webdriver.chrome.options import Options # Options for intialzing browser
from selenium.webdriver.common.by import By # Search for things using specific parameters
from selenium.webdriver.common.keys import Keys # Send key commands easily
from selenium.webdriver.support.ui import WebDriverWait # Wait for a page to load
from selenium.webdriver.support import expected_conditions as EC # Specify what you are looking for on a specific page in order to determine that the webpage has loaded
from selenium.common.exceptions import TimeoutException # Handling a timeout situation

class WebScraper:
    def __init__(self, is_headless=True, config_file="config.json"):
        OPTIONS = Options()
        OPTIONS.headless = is_headless
        OPTIONS.add_argument("start-maximized")

        with open(config_file,'r') as f:
            self.config = json.load(f)

        DRIVER_PATH = self.config['assets']['driver']
        self.driver = webdriver.Chrome(DRIVER_PATH, options=OPTIONS)
        
        self.driver.implicitly_wait(10)
    
    def login(self, credentials_file="credentials.json"):
        # Load json credentials
        with open(credentials_file,'r') as f:
            credentials = json.load(f)

        pandora_login_url = self.config['URLs']['pandora']['login']
        self.driver.get(pandora_login_url)
        self.driver.find_element_by_name('username').send_keys(credentials['pandora']['username'])
        self.driver.find_element_by_name('password').send_keys(credentials['pandora']['password'])
        self.driver.find_element_by_css_selector("button[data-qa='login_button']").click()
        
        # try:
        # Using implciit wait and explicit wait together causes errors
        #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nowPlayingTopInfo__artContainer__art")))
        # except:
        #     self.close_browser()

    def logout(self):
        pandora_logout_url = self.config['URLs']['pandora']['logout']
        self.driver.get(pandora_logout_url)
    
    def close_browser(self):
        self.driver.quit()
    
    def get_stations(self):
        # Click My Collections
        self.driver.find_element(By.CSS_SELECTOR, "a[data-qa='header_my_stations_link']").click()

        self.scroll_to_bottom()

        station_elements = self.driver.find_elements(By.CLASS_NAME, 'InfiniteGrid__contents__itemContainer')
        
        stations = [self.driver.find_element(By.CLASS_NAME, "GridItem__caption__link").get_attribute('href') for element in station_elements]
        
        print(len(stations))
        # for element in station_elements:
        #     # stations += adds the letters instead of full string
        #     stations.append(self.driver.find_element(By.CLASS_NAME, "GridItem__caption__link").get_attribute('href'))
        
        return stations
        
    def scroll_to_bottom(self, timeout=15):
        SCROLL_PAUSE_TIME = random.uniform(0.5, 1.5)
        
        while True:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                break


    def go_to_URL(self, URL):
        self.driver.get(URL)

    