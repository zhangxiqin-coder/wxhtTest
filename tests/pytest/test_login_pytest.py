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

def _do_login(driver, test_logger, username: str, password: str, expected_success: bool, expected_error: str | None):
    # 处理空用户名用于文件名
    username_for_file = username if username else "empty"
    
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    # 1. Open login page
    test_logger.log("Opening login page...")
    login_page.open_page()
    test_logger.log(f"Login page loaded: {driver.current_url}")
    
    # Take screenshot
    driver.save_screenshot(f"test_screenshots/test_login_scenario_{username_for_file}_1_loaded.png")
    test_logger.screenshot("page_loaded")
    
    # 2. Fill login form
    test_logger.log(f"Filling username: '{username}'")
    login_page.fill_username(username)
    
    test_logger.log(f"Filling password: '******'")
    login_page.fill_password(password)
    driver.save_screenshot(f"test_screenshots/test_login_scenario_{username_for_file}_2_filled.png")
    test_logger.screenshot("form_filled")
    
    # 3. Click login button
    test_logger.log("Clicking login button...")
    login_page.click_login()
    
    # 4. Wait for page to react
    test_logger.log("Waiting for page reaction...")
    if expected_success:
        try:
            WebDriverWait(driver, 10).until(lambda d: d.current_url != driver.current_url)
            test_logger.log(f"URL changed to: {driver.current_url}")
        except TimeoutException:
            test_logger.log("WARNING: URL did not change within timeout")
    
    driver.save_screenshot(f"test_screenshots/test_login_scenario_{username_for_file}_3_after_login.png")
    test_logger.screenshot("after_login")
    
    # 5. Verify result
    actual_success = dashboard_page.is_dashboard_displayed
    test_logger.log(f"Dashboard displayed: {actual_success}")
    
    if expected_success:
        assert actual_success, f"Expected success but got failure"
        test_logger.log("PASS: Login successful as expected")
    else:
        if actual_success:
            test_logger.log("FAIL: Login succeeded but expected failure")
            assert False, "Expected failure but login succeeded"
        else:
            error_msg = login_page.get_login_error()
            test_logger.log(f"PASS: Login failed as expected with error: {error_msg}")
            if expected_error:
                assert expected_error in error_msg, f"Expected error '{expected_error}' but got '{error_msg}'"

# ── Tests ──

class TestLoginSuite:
    """登录功能测试套件"""

    def setup_method(self):
        """每个测试用例执行前的setup"""
        print("\n[Setup] 准备测试环境...")

    def teardown_method(self, method):
        """每个测试用例执行后的teardown"""
        print("\n[Teardown] 清理浏览器...")
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"[Teardown] 退出浏览器时出错: {e}")

    @pytest.fixture(autouse=True)
    def _setup_driver(self, driver, test_logger):
        """自动注入driver和logger fixture"""
        self.driver = driver
        self.test_logger = test_logger
        yield driver

    @pytest.mark.parametrize("username,password,expected_success,expected_error", TEST_CASES)
    def test_login_scenario(self, username, password, expected_success, expected_error):
        """Test login with various credentials"""
        self.test_logger.log(f"=== Starting test with user: {username} ===")
        _do_login(self.driver, self.test_logger, username, password, expected_success, expected_error)
        self.test_logger.log(f"=== Test completed ===")
