from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .attack_vector import AttackVector


class Meetup:
    _DRIVER_PATH = "libs/chromedriver"

    def __init__(self):
        self._driver = webdriver.Chrome(Meetup._DRIVER_PATH)
        self._attack_vector = AttackVector()

    def track(self):
        self._login()

        groups = self._get_groups()
        for group in groups[:1]:
            print(f"Group name: {group.text}")
            group.click()

            events = self._get_events()
            for event in events[:1]:
                print("Event name: " + event.text.split("\n")[0])
                event.click()

    def _login(self):
        page_url = self._attack_vector.get_seed_url()
        self._driver.get(page_url)
        assert self._driver.title == "Login to Meetup | Meetup", f"Unexpected page title: '{self._driver.title}'"

        login = self._driver.find_element_by_id("email")
        login.send_keys(self._attack_vector.get_login())

        password = self._driver.find_element_by_id("current-password")
        password.send_keys(self._attack_vector.get_password())
        password.send_keys(Keys.RETURN)

    def _get_groups(self):
        WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.ID, "my-meetup-groups-list")))

        self._driver.find_element(by=By.CLASS_NAME, value="see-more-groups").click()

        groups_list = self._driver.find_element_by_id("my-meetup-groups-list")
        groups = groups_list.find_elements(by=By.CLASS_NAME, value="D_name")
        return [group.find_element(by=By.TAG_NAME, value="a") for group in groups]

    def _get_events(self):
        WebDriverWait(self._driver, 30) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, "groupHome-eventsList-upcomingEventsLink")))

        self._driver.find_element(by=By.CLASS_NAME, value="groupHome-eventsList-upcomingEventsLink").click()

        WebDriverWait(self._driver, 30) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, "list--infinite-scroll")))
        events_list = self._driver.find_element(by=By.CLASS_NAME, value="list--infinite-scroll")
        return events_list.find_elements(by=By.CLASS_NAME, value="card")
