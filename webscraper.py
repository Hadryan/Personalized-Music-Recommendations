# Standard library
import json

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
        OPTIONS.add_argument("--window-size=1360,960")

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
    
    def logout(self):
        pandora_logout_url = self.config['URLs']['pandora']['logout']
        self.driver.get(pandora_logout_url)
    
    def close_browser(self):
        self.driver.quit()
    
    def get_stations(self):
        collections_url = self.config['URLs']['pandora']['collections']
        self.driver.get(collections_url)
        stations = self.driver.find_elements(By.CLASS_NAME, 'InfiniteGrid__contents__itemContainer')
        for station in stations:
            print(station)
    
    def go_to_URL(self, URL):
        self.driver.get(URL)

    