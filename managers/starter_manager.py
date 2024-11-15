from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class StarterManager:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def start(self):
        print("Starting the game...")
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")

        try:
            consent_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fc-button-label"))
            )
            consent_button.click()
        except TimeoutException:
            print("Consent button not found or clickable!")

        try:
            lang_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.ID, "langSelect-EN"))
            )
            lang_button.click()
        except TimeoutException:
            print("Language selection button not found or clickable!")

        try:
            cookie_element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.ID, "bigCookie"))
            )
        except TimeoutException:
            print("Big cookie element not found!")

        actions: ActionChains = ActionChains(self.driver)
        return cookie_element, actions

    def end(self):
        print("Ending the game...")
        self.driver.quit()
