"""Test settings page - page loading, sections visibility"""
import time
import pytest
from pages.settings_page import SettingsPage
from helpers import do_login


@pytest.fixture(scope="class")
def suite_login(class_driver):
    """Suite setup - 登录一次，所有测试共享同一个会话"""
    print("\n=== Suite Setup: 登录系统 ===")
    do_login(class_driver)
    print("=== Suite Setup: 登录完成 ===")
    yield class_driver
    print("=== Suite Teardown: 退出浏览器 ===")
    class_driver.quit()


class TestSettingsSuite:
    """设置页面测试套件"""

    @pytest.fixture(autouse=True)
    def _setup_driver(self, suite_login, test_logger):
        """自动注入suite_login和logger fixture"""
        self.driver = suite_login
        self.test_logger = test_logger
        yield suite_login

    def test_settings_page_loads(self):
        """Settings page should load with correct URL"""
        self.test_logger.log("=== Starting test: test_settings_page_loads ===")
        settings = SettingsPage(self.driver)
        settings.open_page()
        self.test_logger.log(f"Settings page loaded: {self.driver.current_url}")
        
        assert settings.is_on_settings_page, f"Expected /settings, got {self.driver.current_url}"
        assert settings.page_title.is_displayed(), "Page title not visible"
        self.test_logger.log("PASS: Settings page loaded successfully")

    def test_save_settings_button_visible(self):
        """Save settings button should be visible"""
        self.test_logger.log("=== Starting test: test_save_settings_button_visible ===")
        settings = SettingsPage(self.driver)
        settings.open_page()
        self.test_logger.log("Settings page opened")
        
        assert settings.save_settings_btn.is_displayed(), "Save settings button not visible"
        self.test_logger.log("PASS: Save settings button is visible")

    def test_change_password_button_visible(self):
        """Change password button should be visible"""
        self.test_logger.log("=== Starting test: test_change_password_button_visible ===")
        settings = SettingsPage(self.driver)
        settings.open_page()
        self.test_logger.log("Settings page opened")
        
        assert settings.change_password_btn.is_displayed(), "Change password button not visible"
        self.test_logger.log("PASS: Change password button is visible")

    def test_delete_permission_switch_visible(self):
        """Super admin delete permission switch should be visible"""
        self.test_logger.log("=== Starting test: test_delete_permission_switch_visible ===")
        settings = SettingsPage(self.driver)
        settings.open_page()
        self.test_logger.log("Settings page opened")
        
        assert settings.delete_permission_switch.is_displayed(), "Delete permission switch not visible"
        self.test_logger.log("PASS: Delete permission switch is visible")

    def test_reset_defaults_button_visible(self):
        """Reset defaults button should be visible"""
        self.test_logger.log("=== Starting test: test_reset_defaults_button_visible ===")
        settings = SettingsPage(self.driver)
        settings.open_page()
        self.test_logger.log("Settings page opened")
        
        assert settings.reset_defaults_btn.is_displayed(), "Reset defaults button not visible"
        self.test_logger.log("PASS: Reset defaults button is visible")
