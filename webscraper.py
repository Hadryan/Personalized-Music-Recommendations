# Standard library
import json
import time
import random
import sys

# Related third party
from bs4 import BeautifulSoup  # html/xml parser
# Launch/initialise a browser and affect javascript easily
from selenium import webdriver
# Options for intialzing browser
from selenium.webdriver.chrome.options import Options
# Search for things using specific parameters
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Send key commands easily
from selenium.webdriver.support.ui import WebDriverWait  # Wait for a page to load
# Specify what you are looking for on a specific page in order to determine that the webpage has loaded
from selenium.webdriver.support import expected_conditions as EC
# Handling a timeout situation
from selenium.common.exceptions import TimeoutException


class WebScraper:
    def __init__(self, is_headless=True):
        OPTIONS = Options()
        OPTIONS.headless = is_headless
        OPTIONS.add_argument("--mute-audio")

        if is_headless:
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            OPTIONS.add_argument(f"user-{user_agent}")
            OPTIONS.add_argument("window-size=2560x1440")
            OPTIONS.add_argument("--log-level=3")
        else:
            OPTIONS.add_argument("--start-maximized")

        DRIVER_PATH = "assets\\chromedriver.exe"
        self.driver = webdriver.Chrome(DRIVER_PATH, options=OPTIONS)

        self.driver.implicitly_wait(10)

    def login(self, credentials_file=r"authentication\credentials.json"):
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)

        pandora_login_url = "https://www.pandora.com/account/sign-in"
        self.driver.get(pandora_login_url)
        self.driver.find_element_by_name("username").send_keys(
            credentials['pandora']['username'])
        self.driver.find_element_by_name("password").send_keys(
            credentials['pandora']['password'])
        self.driver.find_element_by_css_selector(
            "button[data-qa='login_button']").click()

    def logout(self):
        pandora_logout_url = "https://www.pandora.com/account/sign-out"
        self.driver.get(pandora_logout_url)

    def close_browser(self):
        self.driver.quit()

    def get_stations_URLs(self):
        self.driver.find_element(
            By.CSS_SELECTOR, "a[data-qa='header_my_stations_link']").click()

        self.scroll_page()

        station_elements = self.driver.find_elements(
            By.CLASS_NAME, "GridItem__caption__link")
        stations_URL = [element.get_attribute(
            "href") for element in station_elements]

        return stations_URL

    def get_songs(self, stations_URL):
        data = {'stations': []}
        errors = []

        for station_URL in stations_URL:
            try:
                self.go_to_URL(station_URL)
                VIEW_PAUSE_TIME = random.uniform(1, 2)
                time.sleep(VIEW_PAUSE_TIME)

                temp = self.driver.find_elements(
                    By.CLASS_NAME, "DisplayThumb__flexWrap__count")
                thumbs_up_count, thumbs_down_count = int(
                    temp[0].text), int(temp[1].text)

                if thumbs_up_count == 0 and thumbs_down_count == 0:
                    continue
                up_songs, up_artists, down_songs, down_artists = [], [], [], []

                try:
                    name = self.driver.find_element(
                        By.CLASS_NAME, "EditableTitle__input").get_attribute("value")
                except:
                    name = self.driver.find_element(
                        By.CLASS_NAME, "StationDetailsHeader__title__mainTitle__text").text
                print(
                    f"{name}\n\tLikes: {thumbs_up_count} Dislike: {thumbs_down_count}")

                if thumbs_up_count > 0:
                    feedback_list = self.driver.find_element(
                        By.CLASS_NAME, "FeedbackList__list")
                    self.scroll_element(feedback_list)
                    up_songs, up_artists = self.collect_feedback_list(
                        feedback_list)

                if thumbs_down_count > 0:
                    down_button = self.driver.find_element(By.CLASS_NAME, "FeedbackList__ListHeader").find_element(
                        By.CLASS_NAME, "DisplayThumb--down")
                    self.scroll_element_into_middle(down_button)
                    down_button.click()

                    feedback_list = self.driver.find_element(
                        By.CLASS_NAME, "FeedbackList__list")

                    self.scroll_element(feedback_list)
                    down_songs, down_artists = self.collect_feedback_list(
                        feedback_list)
                print(
                    f"\tActual Likes: {len(up_songs)} Actual Dislike: {len(down_songs)}")
                data['stations'].append({
                    'name': name,
                    'URL': station_URL,
                    'songs': {'name': up_songs + down_songs, 'artist': up_artists + down_artists, 'liked': ([True]*len(up_songs)) + [False]*len(down_songs)}
                })
            except KeyboardInterrupt:
                print(sys.exc_info())
                break
            except:
                exception = str(sys.exc_info())
                errors.append({station_URL: exception})
                continue

        with open(r'inputs\data.json', 'w', encoding='utf-8') as f1, open(r'outputs\errors.json', 'w', encoding='utf-8') as f2:
            json.dump(data, f1, ensure_ascii=False, indent=1)
            json.dump(errors, f2, ensure_ascii=False, indent=1)

    def collect_feedback_list(self, feedback_list):
        time.sleep(random.uniform(0.75, 1.5))

        songs = feedback_list.find_elements(
            By.CLASS_NAME, "RowItemCenterColumn__mainText")
        artists = feedback_list.find_elements(
            By.CLASS_NAME, "RowItemCenterColumn__secondText")

        songs = [element.text for element in songs]
        artists = [element.text for element in artists]
        return songs, artists

    def scroll_element_into_middle(self, element):
        time.sleep(random.uniform(0.75, 1.5))

        script = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);" + \
            "var elementTop = arguments[0].getBoundingClientRect().top;" + \
            "window.scrollBy(0, elementTop-(viewPortHeight/2));"
        self.driver.execute_script(script, element)

    def scroll_element(self, element):
        self.scroll_element_into_middle(element)
        element.click()
        while True:
            SCROLL_PAUSE_TIME = random.uniform(0.75, 1.5)
            new_height = element.size['height']
            webdriver.ActionChains(self.driver).move_to_element(element).send_keys(
                Keys.END).send_keys(Keys.ARROW_UP).send_keys(Keys.END).perform()
            time.sleep(SCROLL_PAUSE_TIME)
            last_height = element.size['height']
            # print(f"{element} --- {last_height} --- {new_height}")
            if last_height == new_height:
                time.sleep(SCROLL_PAUSE_TIME)
                return

    def scroll_page(self):
        while True:
            SCROLL_PAUSE_TIME = random.uniform(0.75, 1.5)

            scroll_height = "return document.body.scrollHeight;"
            scroll_down = "window.scrollTo(0, document.body.scrollHeight);"

            last_height = self.driver.execute_script(scroll_height)
            self.driver.execute_script(scroll_down)
            time.sleep(SCROLL_PAUSE_TIME)
            self.driver.execute_script("window.scroll(0, -10);")
            time.sleep(SCROLL_PAUSE_TIME)
            self.driver.execute_script(scroll_down)
            new_height = self.driver.execute_script(scroll_height)
            if last_height == new_height:
                return

    def go_to_URL(self, URL):
        self.driver.get(URL)

    def build(self):
        self.webscraper.login()
        station_URLs = self.webscraper.get_stations_URLs()
        self.webscraper.get_songs(station_URLs)
        input('Press ENTER to exit browser')
        self.webscraper.close_browser()
