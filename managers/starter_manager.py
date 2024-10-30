from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


class StarterManager:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def start(self):
        print("Starting the game...")
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        time.sleep(1)

        self.driver.find_element(By.CLASS_NAME, "fc-button-label").click()

        self.driver.find_element(By.ID, "langSelect-EN").click()
        time.sleep(3)

        cookie_element = self.driver.find_element(By.ID, "bigCookie")
        actions: ActionChains = ActionChains(self.driver)

        return cookie_element, actions

    def end(self):
        print("Ending the game...")
        self.driver.quit()
