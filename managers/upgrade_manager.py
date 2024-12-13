import re
import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.upgrade_option import UpgradeOption


class UpgradeManager:
    def __init__(self, upgrade_option: UpgradeOption, driver):
        self.upgrade_option = upgrade_option
        self.driver = driver

    def set_upgrade_option(self, upgrade_option):
        self.upgrade_option = upgrade_option

    def upgrade(self) -> None:
        """Upgrade the selected element."""
        if self.upgrade_option:
            try:
                print(f"Upgrading option: {self.upgrade_option.name}")
                self.upgrade_option.upgrade()
            except Exception as e:
                print(f"Error during upgrade: {e}")

    def auto_upgrade(self):
        """Automatically upgrade the most profitable option."""
        print("Auto-upgrading...")
        most_profitable_option = self.most_profitable_option()
        if most_profitable_option:
            self.set_upgrade_option(most_profitable_option)
            self.upgrade()
        else:
            print("No profitable upgrade option found.")

    def most_profitable_option(self) -> UpgradeOption:
        """Select the most profitable CPS/Cost ratio option."""
        print("Finding the most profitable option...")

        # Check store upgrades 1s
        store_upgrades = self.list_available_store_upgrade_options()
        if store_upgrades:
            print("Selecting the most profitable store upgrade...")
            return store_upgrades[0]

        # Fallback
        upgrade_options = self.list_available_upgrade_options()
        if upgrade_options:
            upgrade_options.sort(key=lambda x: x.cps / x.cost if x.cost > 0 else 0, reverse=True)
            print(f"Selected upgrade: {upgrade_options[0].name} (CPS: {upgrade_options[0].cps}, Cost: {upgrade_options[0].cost})")
            return upgrade_options[0]

        print("No profitable upgrade option found.")
        return None

    def list_available_upgrade_options(self) -> list[UpgradeOption]:
        """List all available upgrade options."""
        print("Listing available upgrade options...")
        try:
            products = self.driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
            upgrade_options = []

            for product in products:
                try:
                    price_text = product.find_element(By.CSS_SELECTOR, ".price").text
                    price = int(re.sub(r'\D', '', price_text)) if price_text else 0

                    owned_text = product.find_element(By.CSS_SELECTOR, ".title.owned").text
                    owned = int(owned_text) if owned_text.isdigit() else 0

                    product_id = int(product.get_attribute("id").replace("product", ""))
                    cps = self.driver.execute_script(f"return Game.ObjectsById[{product_id}].storedCps;")

                    upgrade_option = UpgradeOption(
                        name=product.find_element(By.CSS_SELECTOR, ".title.productName").text,
                        id=product.get_attribute("id"),
                        cps=cps if cps else 0,
                        cost=price,
                        owned=owned,
                        element=product,
                        driver=self.driver
                    )
                    upgrade_options.append(upgrade_option)
                except Exception as e:
                    print(f"Error processing product: {e}")

            return upgrade_options
        except Exception as e:
            print(f"Error listing upgrade options: {e}")
            return []

    def list_available_store_upgrade_options(self) -> list[UpgradeOption]:
        """List all available store upgrade options."""
        print("Listing available store upgrade options...")
        try:
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
                except Exception as e:
                    print(f"Error processing store upgrade: {e}")

            return upgrade_options
        except Exception as e:
            print(f"Error listing store upgrade options: {e}")
            return []

    def legacy_upgrade(self):
        """Handle the legacy upgrade process."""
        try:
            legacy_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "legacyButton"))
            )
            legacy_button.click()

            ascend_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#promptOption0.option.smallFancyButton"))
            )
            ascend_button.click()

            reincarnate_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ascendButton"))
            )
            reincarnate_button.click()

            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "promptOption1"))
            )
            confirm_button.click()

            print("Legacy upgrade completed successfully.")
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f"Error in legacy_upgrade: {e}")
