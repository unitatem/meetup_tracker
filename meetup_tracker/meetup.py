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
        page_url = self._attack_vector.get_seed_url()
        self._login(page_url)

        groups = self._get_groups()
        for group in groups[:1]:
            print(f"Group: {group}")
            events = self._get_events(group)
            for event in events[:2]:
                print(f"Event: {event}")
                attendees = self._get_attendees(event)
                print(attendees)

    def _login(self, url):
        self._driver.get(url)
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
        return [group.find_element(by=By.TAG_NAME, value="a").get_attribute("href") for group in groups]

    def _get_events(self, group_url):
        self._driver.get(group_url)

        WebDriverWait(self._driver, 30) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, "groupHome-eventsList-upcomingEventsLink")))

        self._driver.find_element(by=By.CLASS_NAME, value="groupHome-eventsList-upcomingEventsLink").click()

        WebDriverWait(self._driver, 30) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, "list--infinite-scroll")))
        events_list = self._driver.find_element(by=By.CLASS_NAME, value="list--infinite-scroll")
        return [event.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                for event in events_list.find_elements(by=By.CLASS_NAME, value="card")]

    def _get_attendees(self, event_url):
        self._driver.get(event_url)

        if self._is_event_cancelled():
            return

        self._driver.get(event_url + "attendees/")
        WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "attendees-list")))
        attendees_list = self._driver.find_element(by=By.CLASS_NAME, value="attendees-list")
        attendees = attendees_list.find_elements(by=By.CLASS_NAME, value="attendee-item")
        return [attendee.text.split("\n")[0] for attendee in attendees]

    def _is_event_cancelled(self):
        WebDriverWait(self._driver, 30) \
            .until(EC.presence_of_element_located((By.CLASS_NAME, "eventTimeDisplay")))
        elements = self._driver.find_elements(by=By.CLASS_NAME, value="eventTimeDisplay-canceled")
        return len(elements) == 1
