# Standard library
import json
import time
import random
import sys
import pathlib

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
        self.DATA_PATH = r"inputs\data.json"

    def login(self, credentials_file=r"authentication\credentials.json"):
        try:
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)

            pandora_login_url = r"https://www.pandora.com/account/sign-in"
            self.driver.go_to_url(pandora_login_url)
            self.driver.find_element(By.NAME, "username").send_keys(
                credentials['pandora']['username'])
            self.driver.find_element(By.NAME, "password").send_keys(
                credentials['pandora']['password'])
            self.driver.find_element(By.CSS_SELECTOR,
                                     "button[data-qa='login_button']").click()

            self.station_urls = self.get_station_urls()
            print("Pandora login successful.")
            print(f"There are {len(self.station_urls)} stations.")

        except Exception as e:
            print(e)

    def logout(self):
        pandora_logout_url = r"https://www.pandora.com/account/sign-out"
        self.driver.go_to_url(pandora_logout_url)

    def close_browser(self):
        self.driver.quit()

    def get_station_urls(self):
        self.driver.find_element(
            By.CSS_SELECTOR, "a[data-qa='header_my_stations_link']").click()

        self.scroll_page()

        station_elements = self.driver.find_elements(
            By.CLASS_NAME, "GridItem__caption__link")
        station_urls = [element.get_attribute(
            "href") for element in station_elements]

        return station_urls

    def get_songs(self, stations_url):
        data = {'stations': []}
        errors = []

        for station_url in stations_url:
            try:
                self.go_to_url(station_url)
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

                    feedback_list = self.driver.find_element(
                        By.CLASS_NAME, "FeedbackList__list")
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
                    feedback_list = self.driver.find_element(
                        By.CLASS_NAME, "FeedbackList__list")

                    down_songs, down_artists = self.collect_feedback_list(
                        feedback_list)
                print(
                    f"\tActual Likes: {len(up_songs)} Actual Dislike: {len(down_songs)}")
                data['stations'].append({
                    'name': name,
                    'url': station_url,
                    'songs': {'name': up_songs + down_songs, 'artist': up_artists + down_artists, 'liked': ([True]*len(up_songs)) + [False]*len(down_songs)}
                })
            except KeyboardInterrupt:
                print(sys.exc_info())
                break
            except:
                exception = str(sys.exc_info())
                errors.append({station_url: exception})
                continue
        try:
            with open(self.DATA_PATH, 'w', encoding='utf-8') as f1, open(r'outputs\errors.json', 'w', encoding='utf-8') as f2:
                json.dump(data, f1, ensure_ascii=False, indent=1)
                json.dump(errors, f2, ensure_ascii=False, indent=1)
            print("The data JSON has been created.")
        except EnvironmentError as e:
            print("Something is wrong with the creation of the data and errors file.")
            print(e)

    def collect_feedback_list(self, feedback_list):
        feedback_html = feedback_list.get_attribute("outerHTML")
        soup = BeautifulSoup(feedback_html, "html.parser")

        songs = soup.find_all("div", attrs={
            "class": "RowItemCenterColumn__mainText"})
        artists = soup.find_all("div", attrs={
            "class": "RowItemCenterColumn__secondText"})

        songs = [song.text for song in songs]
        artists = [artist.text for artist in artists]

        return songs, artists
    # def collect_feedback_list(self, feedback_list):
    #     time.sleep(random.uniform(0.75, 1.5))

    #     songs = feedback_list.find_elements(
    #         By.CLASS_NAME, "RowItemCenterColumn__mainText")
    #     artists = feedback_list.find_elements(
    #         By.CLASS_NAME, "RowItemCenterColumn__secondText")

    #     songs = [element.text for element in songs]
    #     artists = [element.text for element in artists]
    #     return songs, artists

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

    def go_to_url(self, url):
        self.driver.get(url)
        time.sleep(random.uniform(3, 7.5))

    def build(self):
        data_file = pathlib.Path(self.DATA_PATH)
        if not data_file.exists() or input("The data JSON already exists. Do you want to overwrite it? Type Y or press ENTER for no.\n") == 'Y':
            self.login()
            self.get_songs(self.station_urls)
            input('Press ENTER to exit browser')
            self.close_browser()
        else:
            print("Did not replace JSON.")
