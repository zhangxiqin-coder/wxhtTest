from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UtilityPage(BasePage):
    """Water/electricity management page PO (tab panel under /rooms)"""

    def open_page(self):
        self.open("https://fangdong.fun/rooms#utility")
