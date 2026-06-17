from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class TenantsPage(BasePage):
    """Tenant management page PO (tab panel under /rooms)"""

    def open_page(self):
        """Open tenants tab via direct URL"""
        self.open("https://fangdong.fun/rooms#tenants")

    @property
    def is_on_tenants_page(self):
        return "/rooms" in self.current_url
