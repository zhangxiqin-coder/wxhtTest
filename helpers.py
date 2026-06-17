"""Login helper - reusable fixture for all dashboard tests"""
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.dashboard_tabs_page import DashboardTabsPage
from pages.nav_component import NavComponent


def do_login(driver, username="testuser3", password="123456"):
    """Login helper - navigate to login page and log in"""
    login_page = LoginPage(driver)
    login_page.open_page()
    time.sleep(1)
    login_page.login(username, password)
    
    # Wait for redirect to complete (away from /login)
    try:
        WebDriverWait(driver, 10).until(lambda d: "/rooms" in d.current_url)
    except TimeoutException:
        pass
    time.sleep(1)


@pytest.fixture
def logged_in_driver(driver):
    """Fixture: login before test, teardown automatically handled by conftest.py"""
    do_login(driver)
    return driver
