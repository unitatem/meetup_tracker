from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    print("App is running...")

    driver_path = "libs/chromedriver"
    driver = webdriver.Chrome(driver_path)

    page_url = "https://www.python.org"
    driver.get(page_url)

    print(driver.title)

    search_bar = driver.find_element_by_name("q")
    search_bar.clear()
    search_bar.send_keys("getting started with python")
    search_bar.send_keys(Keys.RETURN)

    input("Press Enter to continue...")
