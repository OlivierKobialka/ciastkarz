from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from managers.cookie_manager import CookieManager
from managers.starter_manager import StarterManager
from managers.upgrade_manager import UpgradeManager

driver: WebDriver = webdriver.Chrome()
starter_manager: StarterManager = StarterManager(driver)
cookie_element, actions = starter_manager.start()
cookie = CookieManager(cookie_element, driver, actions)
upgrade_manager = UpgradeManager([], driver)

while True:
    print("Clicking cookie...")
    for _ in range(10):
        actions.click(cookie_element).perform()

    cookie_count = cookie.get_cookie_count()
    print(f"Current cookie count: {cookie_count}")

    print("Available Upgrade Options:")
    upgrade_options = upgrade_manager.list_available_upgrade_options()

    best_option = upgrade_manager.most_profitable_option()
    if best_option:
        upgrade_manager.set_upgrade_option(best_option)
        print("Most Profitable Upgrade Option:", best_option.get_current_values())
        upgrade_manager.upgrade()
    # upgrade_manager.legacy_upgrade()

driver.quit()
