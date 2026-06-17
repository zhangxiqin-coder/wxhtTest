from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class PaymentsPage(BasePage):
    """Payment records page PO (tab panel under /rooms)"""

    def open_page(self):
        self.open("https://fangdong.fun/rooms#payments")
