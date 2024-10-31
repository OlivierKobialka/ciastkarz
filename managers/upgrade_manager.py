import re
import time

from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.upgrade_option import UpgradeOption
from selenium.webdriver.common.by import By


class UpgradeManager:
    def __init__(self, upgrade_option: UpgradeOption, driver):
        self.upgrade_option = upgrade_option
        self.driver = driver

    def set_upgrade_option(self, upgrade_option):
        self.upgrade_option = upgrade_option

    def upgrade(self) -> None:
        """
        Upgrade the selected element
        :return: None
        """
        if self.upgrade_option:
            print(f"Upgrading option: {self.upgrade_option.name}")
            self.upgrade_option.upgrade()

    def auto_upgrade(self):
        """
        Automatically upgrade the most profitable option.
        :return: None
        """
        print("Auto-upgrading...")
        most_profitable_option = self.most_profitable_option()
        if most_profitable_option:
            self.set_upgrade_option(most_profitable_option)
            self.upgrade()
        else:
            print("No profitable upgrade option found.")

    def most_profitable_option(self) -> UpgradeOption:
        """
        CPS/Cost ratio or if possible then upgrade from store options
        :return:
        """
        print("Finding the most profitable option...")

        # Check store upgrades first
        store_upgrades = self.list_available_store_upgrade_options()
        if store_upgrades:
            print("Store upgrades are available. Selecting the most profitable store upgrade option...")
            # Select the first store upgrade as all of them should be profitable
            most_profitable_store_upgrade = store_upgrades[0]
            print(f"Selected most profitable store upgrade option: {most_profitable_store_upgrade.name}")
            return most_profitable_store_upgrade

        # If no store upgrades are available, check other upgrade options
        print("No store upgrades available. Checking other unlocked upgrade options...")
        upgrade_options = self.list_available_upgrade_options()

        for option in upgrade_options:
            print(f"Option: {option.name}, Cost: {option.cost}, CPS: {option.cps}, Owned: {option.owned}")

        upgrade_options.sort(key=lambda x: x.cps / x.cost if x.cost > 0 else 0, reverse=True)
        print("Sorted upgrade options by CPS/cost ratio...")
        print(upgrade_options)
        for upgrade_option in upgrade_options:
            print(f"Selected most profitable option: {upgrade_option.name}")
            return upgrade_option

        print("No profitable upgrade option found.")
        return None

    def list_available_upgrade_options(self) -> list[UpgradeOption]:
        """
        List all available upgrade options on the page.
        :return: list of UpgradeOption objects
        """
        print("Listing available upgrade options...")
        products = self.driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
        upgrade_options = []

        for product in products:
            try:
                price_text = product.find_element(By.CSS_SELECTOR, ".price").text
                price_match = re.search(r'\d+', price_text)
                price = int(price_match.group()) if price_match else 0

                owned_text = product.find_element(By.CSS_SELECTOR, ".title.owned").text
                owned = int(owned_text) if owned_text.isdigit() else 0

                upgrade_option = UpgradeOption(
                    name=product.find_element(By.CSS_SELECTOR, ".title.productName").text,
                    id=product.get_attribute("id"),
                    cps=int(price),
                    cost=price,
                    owned=owned,
                    element=product,
                    driver=self.driver
                )
                upgrade_options.append(upgrade_option)

                print(f"Found upgrade option - Name: {upgrade_option.name}, Cost: {upgrade_option.cost}, "
                      f"CPS: {upgrade_option.cps}, Owned: {upgrade_option.owned}")

            except Exception as e:
                print(f"Error retrieving product info: {e}")

        return upgrade_options

    def list_available_store_upgrade_options(self) -> list[UpgradeOption]:
        """
        List all available store upgrade options on the page.
        :return: list of UpgradeOption objects but incomplete
        """
        print("Listing available store upgrade options...")
        store_upgrades = self.driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
        upgrade_options = []

        for upgrade in store_upgrades:
            try:
                upgrade_option = UpgradeOption(
                    name=f"Upgrade {upgrade.get_attribute('data-id')}",
                    id=upgrade.get_attribute("id"),
                    cps=0,
                    cost=0,
                    owned=0,
                    element=upgrade,
                    driver=self.driver
                )
                upgrade_options.append(upgrade_option)
                print(f"Found store upgrade option - ID: {upgrade_option.id}")

            except Exception as e:
                print(f"Error retrieving store upgrade info: {e}")

        return upgrade_options


    def legacy_upgrade(self):
        # DOESNT WORK YET
        """
        Click on "Legacy" upgrade option, then after modal pops up, click on "Ascend" button, wait for 5 seconds,
        and click on "Reincarnate" button then "Yes" button.
        """
        try:
            # Check if the Legacy upgrade button is available and visible
            legacy_button = self.driver.find_elements(By.ID, "legacyButton")
            if not legacy_button or not legacy_button[0].is_displayed():
                print("Legacy upgrade button not available or not visible. Waiting for the next opportunity to ascend.")
                return

            print("Attempting to click the Legacy upgrade button...")
            legacy_upgrade = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "legacyButton"))
            )
            legacy_upgrade.click()
            print("Legacy upgrade button clicked.")

            print("Waiting for Ascend button to appear...")
            ascend_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#promptOption0.option.smallFancyButton"))
            )
            ascend_button.click()
            print("Ascend button clicked.")

            time.sleep(5)

            print("Waiting for Reincarnate button to appear...")
            reincarnate_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ascendButton"))
            )
            reincarnate_button.click()
            print("Reincarnate button clicked.")

            print("Waiting for final confirmation button...")
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "promptOption1"))
            )
            confirm_button.click()
            print("Confirmation button clicked. Ascension process completed.")

            time.sleep(10)

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Error in legacy_upgrade: {e}")
