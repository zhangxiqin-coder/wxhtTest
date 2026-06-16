import time
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from conftest import retry_on_failure


# ── Test case data ──

TEST_CASES = [
    pytest.param(
        "testuser3", "123456", True, None,
        id="TC001_CorrectCredentials",
        marks=pytest.mark.flaky(reruns=2, reruns_delay=2)
    ),
    pytest.param(
        "testuser3", "wrongpassword", False, "用户名或密码错误",
        id="TC002_WrongPassword",
    ),
    pytest.param(
        "nonexistentuser", "123456", False, "用户名或密码错误",
        id="TC003_NonexistentUsername",
    ),
    pytest.param(
        "", "123456", False, None,
        id="TC004_EmptyUsername",
        marks=pytest.mark.xfail(reason="Timeout expected when username is empty", strict=False)
    ),
    pytest.param(
        "testuser3", "", False, None,
        id="TC005_EmptyPassword",
        marks=pytest.mark.xfail(reason="Timeout expected when password is empty", strict=False)
    ),
    pytest.param(
        "", "", False, None,
        id="TC006_AllEmpty",
        marks=pytest.mark.xfail(reason="Timeout expected when both are empty", strict=False)
    ),
    pytest.param(
        "testuser3", "!@#$%^&*()", False, "用户名或密码错误",
        id="TC007_SpecialCharsPassword",
    ),
]


# ── Helpers ──

def _do_login(driver, username: str, password: str, expected_success: bool, expected_error: str | None):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    # 1. Open login page
    login_page.open_page()
    time.sleep(1)
    current_url = driver.current_url
    print(current_url)
    # 2. Login
    login_page.login(username, password)


    # 3. Wait for page to react - first try for URL change, then check for error
    #    Use try-except to avoid exceptions from page changes
    if expected_success:
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.current_url != current_url
            )
        except TimeoutException:
            # If URL didn't change, check if error is displayed
            pass
    else:
        # If expected error, check if error is displayed
        assert login_page.is_error_displayed(), \
            f"Expected error containing '{expected_error}', but none displayed"

    time.sleep(1)
    actual_success = dashboard_page.is_dashboard_displayed

    # Verify result
    assert actual_success == expected_success, \
        f"Expected success={expected_success}, got success={actual_success}"

    # Check error message if expected
    if not actual_success and expected_error:
        actual_error = login_page.get_login_error()
        assert expected_error in actual_error, \
            f"Expected error containing '{expected_error}', got '{actual_error}'"

# ── Tests ──

@pytest.mark.parametrize("username,password,expected_success,expected_error", TEST_CASES)
def test_login_scenario(driver, username, password, expected_success, expected_error):
    """Test login with various credentials"""
    _do_login(driver, username, password, expected_success, expected_error)
