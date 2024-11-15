from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from managers.cookie_manager import CookieManager
from managers.starter_manager import StarterManager
from managers.statistics_manager import StatisticsManager
from managers.upgrade_manager import UpgradeManager

driver: WebDriver = webdriver.Chrome()

starter_manager: StarterManager = StarterManager(driver)
cookie_element, actions = starter_manager.start()

cookie_manager = CookieManager(cookie_element, driver, actions)
upgrade_manager = UpgradeManager([], driver)
statistics_manager = StatisticsManager(driver)

try:
    while True:
        for _ in range(10):
            cookie_manager.click_cookie()

        statistics_manager.auto_stats()
        upgrade_manager.auto_upgrade()
        cookie_manager.click_golden_cookie()

except KeyboardInterrupt:
    print("Stopping the bot...")

finally:
    driver.quit()
