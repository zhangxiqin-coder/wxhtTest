from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class DashboardPage(BasePage):
    """登录后主页面 PO"""

    # ── 页面元素声明 ──
    rooms_link = FindBy(By.XPATH, "//a[contains(text(),'房屋') or contains(text(),'rooms')]")
    utility_link = FindBy(By.XPATH, "//a[contains(text(),'工具') or contains(text(),'utility')]")
    user_profile = FindBy(By.XPATH, "//a[contains(text(),'个人') or contains(text(),'profile')]")

    @property
    def is_dashboard_displayed(self):
        """判断是否成功进入主页"""
        return "login" not in self.current_url.lower()

    def get_page_title(self) -> str:
        return self.title
