from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.element import Element


class BasePage:
    """Page Object base class - encapsulates common operations"""

    def __init__(self, driver: WebDriver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(driver, timeout)
        self._init_elements()

    def _init_elements(self):
        """Initialize @FindBy defined attributes (automatically initialized to Element instances)"""
        pass

    def open(self, url: str):
        self.driver.get(url)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def title(self) -> str:
        return self.driver.title

    def switch_to_main_content(self):
        self.driver.switch_to.default_content()

    def refresh(self):
        self.driver.refresh()

    def wait_for_url_contains(self, text: str, timeout=None):
        t = timeout or self.timeout
        WebDriverWait(self.driver, t).until(EC.url_contains(text))
