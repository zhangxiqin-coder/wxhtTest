"""Test settings page - page loading, sections visibility"""
import time
import pytest
from pages.settings_page import SettingsPage
from conftest import retry_on_failure
from helpers import do_login


@retry_on_failure(max_retries=1, delay=2)
def test_settings_page_loads(driver):
    """Settings page should load with correct URL"""
    do_login(driver)
    settings = SettingsPage(driver)
    settings.open_page()
    time.sleep(2)
    
    assert settings.is_on_settings_page, f"Expected /settings, got {driver.current_url}"
    assert settings.page_title.is_displayed(), "Page title not visible"


@retry_on_failure(max_retries=1, delay=2)
def test_save_settings_button_visible(driver):
    """Save settings button should be visible"""
    do_login(driver)
    settings = SettingsPage(driver)
    settings.open_page()
    time.sleep(1)
    
    assert settings.save_settings_btn.is_displayed(), "Save settings button not visible"


@retry_on_failure(max_retries=1, delay=2)
def test_change_password_button_visible(driver):
    """Change password button should be visible"""
    do_login(driver)
    settings = SettingsPage(driver)
    settings.open_page()
    time.sleep(1)
    
    assert settings.change_password_btn.is_displayed(), "Change password button not visible"


@retry_on_failure(max_retries=1, delay=2)
def test_delete_permission_switch_visible(driver):
    """Super admin delete permission switch should be visible"""
    do_login(driver)
    settings = SettingsPage(driver)
    settings.open_page()
    time.sleep(1)
    
    assert settings.delete_permission_switch.is_displayed(), "Delete permission switch not visible"


@retry_on_failure(max_retries=1, delay=2)
def test_reset_defaults_button_visible(driver):
    """Reset defaults button should be visible"""
    do_login(driver)
    settings = SettingsPage(driver)
    settings.open_page()
    time.sleep(1)
    
    assert settings.reset_defaults_btn.is_displayed(), "Reset defaults button not visible"
