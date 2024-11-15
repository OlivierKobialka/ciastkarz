from selenium.webdriver.common.by import By


class CookieManager:
    def __init__(self, cookie, driver, actions):
        self.cookie = cookie
        self.driver = driver
        self.actions = actions

    def click_cookie(self):
        self.actions.click(self.cookie).perform()

    def get_cookie_count(self) -> int:
        return self.driver.find_element(By.ID, "cookies").text.replace(" cookies", "").replace(" cookie", "")

    def click_golden_cookie(self):
        golden_cookie = self.driver.find_element(By.ID, "shimmers")
        if golden_cookie:
            self.actions.click(golden_cookie).perform()
