from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


class StatisticsManager:
    def __init__(self, driver, interval=3600) -> None:
        self.driver = driver
        self.interval = interval
        self.last_stats_time = time.time()

    def open_statistics_menu(self):
        """Opens the statistics menu by clicking the stats button."""
        try:
            stats_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "statsButton"))
            )
            stats_button.click()
            print("Statistics menu opened.")
        except TimeoutException:
            print("Error: 'statsButton' not found or not clickable.")
        except NoSuchElementException:
            print("Error: 'statsButton' element not found.")

    def read_statistics(self) -> None:
        """Reads and prints statistics data from 'menu' and 'statsGeneral' sections."""
        try:
            self.open_statistics_menu()

            menu_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "menu"))
            )
            stats_general_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "statsGeneral"))
            )

            print("Reading statistics from 'menu' section...")
            print(menu_element.text)

            print("Reading statistics from 'statsGeneral' section...")
            print(stats_general_element.text)

        except TimeoutException:
            print("Error: 'menu' or 'statsGeneral' elements not visible within the timeout period.")
        except NoSuchElementException:
            print("Error: 'menu' or 'statsGeneral' elements not found.")

    def get_statistics_data(self) -> dict:
        """Returns the statistics data as a dictionary."""
        stats_data = {}

        try:
            self.open_statistics_menu()

            menu_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "menu"))
            )
            stats_general_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "statsGeneral"))
            )

            stats_data['menu'] = menu_element.text
            stats_data['stats_general'] = stats_general_element.text

        except TimeoutException:
            print("Error: 'menu' or 'statsGeneral' elements not visible within the timeout period.")
        except NoSuchElementException:
            print("Error: 'menu' or 'statsGeneral' elements not found.")

        return stats_data

    def get_achievements(self) -> str:
        """Reads and returns the achievements data from the 'statsAchievements' section."""
        try:
            self.open_statistics_menu()
            stats_achievements_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "statsAchievements"))
            )
            return stats_achievements_element.text
        except TimeoutException:
            print("Error: 'statsAchievements' element not visible within the timeout period.")
        except NoSuchElementException:
            print("Error: 'statsAchievements' element not found.")
        return None

    def auto_stats(self) -> None:
        """Automatically prints statistics every specified interval (default 1 hour)."""
        current_time: float = time.time()
        if current_time - self.last_stats_time >= self.interval:
            print("Printing statistics data...")
            self.read_statistics()
            self.last_stats_time = current_time
        else:
            print("Waiting for next statistics print interval...")

