from selenium.webdriver.common.by import By


class UpgradeOption:
    def __init__(self, name: str, id: str, cps: int, cost: int, owned: int, element, driver) -> None:
        self.name = name
        self.id = id
        self.cps = cps
        self.cost = cost
        self.owned = owned
        self.element = element
        self.driver = driver

    def upgrade(self) -> None:
        if "enabled" in self.element.get_attribute("class"):
            self.element.click()

        self.change_values(
            name=self.name,
            id=self.id,
            cps=self.cps,
            cost=self.cost,
            element=self.driver.find_element(By.ID, self.id),
            owned=self.owned
        )

    def get_current_values(self):
        return self.name, self.id, self.cps, self.cost, self.owned, self.element

    def change_values(self, name, id, cps, cost, element, owned) -> None:
        self.name = name
        self.id = id
        self.cps = cps
        self.cost = cost
        self.element = element
        self.owned = owned
