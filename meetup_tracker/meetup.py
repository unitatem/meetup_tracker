from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .attack_vector import AttackVector


class Meetup:
    _DRIVER_PATH = "libs/chromedriver"

    def __init__(self):
        self._driver = webdriver.Chrome(Meetup._DRIVER_PATH)
        self._attack_vector = AttackVector()

    def track(self):
        page_url = self._attack_vector.get_seed_url()
        self._driver.get(page_url)
        assert self._driver.title == "Login to Meetup | Meetup", f"Unexpected page title: '{self._driver.title}'"
