from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class NavComponent(BasePage):
    """Shared sidebar/top navigation component used across all pages after login"""

    # Sidebar navigation links (el-menu-item)
    rooms_link = FindBy(By.XPATH, "//li[contains(@class, 'el-menu-item') and contains(., '房屋管理')]")
    settings_link = FindBy(By.XPATH, "//li[contains(@class, 'el-menu-item') and contains(., '设置')]")
    rooms_tab = FindBy(By.ID, "tab-rooms")
    tenants_tab = FindBy(By.ID, "tab-tenants")
    payments_tab = FindBy(By.ID, "tab-payments")
    utility_tab = FindBy(By.ID, "tab-utility")

    # User info & actions
    username_display = FindBy(By.CLASS_NAME, "username")
    logout_btn = FindBy(By.XPATH, "//button[contains(., '退出登录')]")
    hide_amount_btn = FindBy(By.XPATH, "//button[contains(., '隐藏金额')]")
