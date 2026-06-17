from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class SettingsPage(BasePage):
    """Settings page PO - system settings, account info, landlord info, password"""

    url = "https://fangdong.fun/settings"

    # ── Settings page sections ──
    page_title = FindBy(By.XPATH, "//h1[contains(., '系统设置')]")
    
    # Reminder settings
    save_settings_btn = FindBy(By.XPATH, "//button[contains(., '保存设置')]")
    reset_defaults_btn = FindBy(By.XPATH, "//button[contains(., '恢复默认')]")

    # Account info
    username_value = FindBy(By.XPATH, "//span[contains(@class, 'info-label') and contains(., '用户名')]/following-sibling::span")
    display_name_input = FindBy(By.XPATH, "//input[@placeholder='请输入显示名称']")
    save_display_name_btn = FindBy(By.XPATH, "(//button[contains(., '保存')])[1]")

    # Landlord info
    landlord_name_input = FindBy(By.XPATH, "//input[@placeholder='请输入甲方姓名']")
    landlord_phone_input = FindBy(By.XPATH, "//input[@placeholder='请输入甲方电话']")
    save_landlord_btn = FindBy(By.XPATH, "(//button[contains(., '保存')])[2]")

    # Password
    change_password_btn = FindBy(By.XPATH, "//button[contains(., '修改密码')]")

    # Super admin
    delete_permission_switch = FindBy(By.XPATH, "//span[contains(@class, 'el-switch')]")

    # Navigation
    logout_btn = FindBy(By.XPATH, "//button[contains(., '退出登录')]")
    hide_amount_btn = FindBy(By.XPATH, "//button[contains(., '隐藏金额')]")

    def open_page(self):
        """Open settings page"""
        self.open(self.url)

    @property
    def is_on_settings_page(self):
        return "/settings" in self.current_url
