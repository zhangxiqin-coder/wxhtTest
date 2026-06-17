"""Test navigation - sidebar links and tab switching after login"""
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.nav_component import NavComponent
from pages.settings_page import SettingsPage
from pages.rooms_page import RoomsPage
from conftest import retry_on_failure
from helpers import do_login


@retry_on_failure(max_retries=1, delay=2)
def test_navigate_to_settings(driver):
    """Navigate to settings page via direct URL"""
    do_login(driver)
    settings = SettingsPage(driver)
    settings.open_page()
    time.sleep(2)
    
    assert settings.is_on_settings_page, f"Expected /settings, got {driver.current_url}"


@retry_on_failure(max_retries=1, delay=2)
def test_navigate_back_to_rooms(driver):
    """Navigate to settings then back to rooms via direct URL"""
    do_login(driver)
    
    # Go to settings directly
    settings = SettingsPage(driver)
    settings.open_page()
    time.sleep(1)
    assert settings.is_on_settings_page
    
    # Go back to rooms
    rooms = RoomsPage(driver)
    rooms.open_page()
    time.sleep(2)
    
    assert rooms.is_on_rooms_page, f"Expected /rooms, got {driver.current_url}"


@retry_on_failure(max_retries=1, delay=2)
def test_switch_to_tenants_tab(driver):
    """Click '租客管理' tab should switch content"""
    do_login(driver)
    nav = NavComponent(driver)
    nav.tenants_tab.click()
    time.sleep(1)
    # The tab should become active - check URL or active class
    tab_class = driver.find_element("id", "tab-tenants").get_attribute("class")
    assert "is-active" in tab_class, f"Tenants tab not active: {tab_class}"


@retry_on_failure(max_retries=1, delay=2)
def test_switch_to_payments_tab(driver):
    """Click '交租记录' tab should switch content"""
    do_login(driver)
    nav = NavComponent(driver)
    nav.payments_tab.click()
    time.sleep(1)
    tab_class = driver.find_element("id", "tab-payments").get_attribute("class")
    assert "is-active" in tab_class, f"Payments tab not active: {tab_class}"


@retry_on_failure(max_retries=1, delay=2)
def test_switch_to_utility_tab(driver):
    """Click '水电管理' tab should switch content"""
    do_login(driver)
    nav = NavComponent(driver)
    nav.utility_tab.click()
    time.sleep(1)
    tab_class = driver.find_element("id", "tab-utility").get_attribute("class")
    assert "is-active" in tab_class, f"Utility tab not active: {tab_class}"


@retry_on_failure(max_retries=1, delay=2)
def test_logout_button_visible(driver):
    """Logout button should be visible after login"""
    do_login(driver)
    nav = NavComponent(driver)
    assert nav.logout_btn.is_displayed(), "Logout button not visible"


@retry_on_failure(max_retries=1, delay=2)
def test_username_displayed(driver):
    """Username should show after login"""
    do_login(driver)
    nav = NavComponent(driver)
    assert nav.username_display.is_displayed(), "Username not displayed"
    username_text = nav.username_display.text
    assert username_text, f"Username text empty, got: '{username_text}'"
