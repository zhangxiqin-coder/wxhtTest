from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Element:
    """Element wrapper - lazy loading WebElement with explicit waits"""

    def __init__(self, driver, locator: tuple, timeout=10):
        self.driver = driver
        self.locator = locator
        self.timeout = timeout
        self._wait = WebDriverWait(driver, timeout)

    @property
    def _element(self):
        return self._wait.until(EC.presence_of_element_located(self.locator))

    def click(self):
        self._wait.until(EC.element_to_be_clickable(self.locator)).click()

    def send_keys(self, value: str):
        element = self._element
        element.clear()
        element.send_keys(value)

    @property
    def text(self):
        return self._element.text

    def is_displayed(self):
        try:
            return self._element.is_displayed()
        except:
            return False

    def is_clickable(self):
        """Check if element is clickable (not blocked, not disabled)"""
        try:
            # Use EC.element_to_be_clickable to check
            self._wait.until(EC.element_to_be_clickable(self.locator))
            return True
        except:
            return False

    @property
    def attribute(self, name: str):
        return self._element.get_attribute(name)

    def __str__(self):
        return f"Element({self.locator})"


class FindBy:
    """@FindBy descriptor - for declarative element definition in Page Objects
    
    Usage:
        class LoginPage(BasePage):
            username_input = FindBy(By.XPATH, "//input[@type='text']")
            login_button = FindBy(By.XPATH, "//button[contains(text(),'登录')]")
    """

    def __init__(self, by: By, value: str):
        self.locator = (by, value)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return Element(obj.driver, self.locator, obj.timeout)
