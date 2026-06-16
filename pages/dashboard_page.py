from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class DashboardPage(BasePage):
    """Dashboard page PO (after successful login)"""

    # ── Page element declarations ──
    rooms_link = FindBy(By.XPATH, "//a[contains(text(),'房屋') or contains(text(),'rooms')]")
    utility_link = FindBy(By.XPATH, "//a[contains(text(),'工具') or contains(text(),'utility')]")
    user_profile = FindBy(By.XPATH, "//a[contains(text(),'个人') or contains(text(),'profile')]")

    @property
    def is_dashboard_displayed(self):
        """Check if successfully entered the dashboard"""
        return "login" not in self.current_url.lower()

    def get_page_title(self) -> str:
        return self.title
