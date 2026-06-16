import time
import os
from dataclasses import dataclass
from typing import List, Optional, Type
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@dataclass
class TestCase:
    """Test case data template"""
    name: str
    username: str
    password: str
    expected_success: bool
    expected_error: Optional[str] = None
    expected_exception: Optional[Type[Exception]] = None
    description: str = ""


class LoginTestSuite:
    """Login test suite (based on Page Object pattern)"""

    def __init__(self):
        self.screenshot_dir = "test_screenshots"
        self.results = []
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    # ── Browser lifecycle ──────────────────────────────

    def _create_driver(self):
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,720')
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _save_screenshot(self, driver, filename: str):
        path = os.path.join(self.screenshot_dir, filename)
        try:
            driver.save_screenshot(path)
            print(f"  📷 Screenshot: {filename}")
        except:
            pass

    # ── Single test case execution ──────────────────────────────

    def _run_test(self, tc: TestCase) -> dict:
        print(f"\n{'='*60}")
        print(f"  {tc.name}")
        print(f"  Description: {tc.description}")
        print(f"{'='*60}")

        result = {
            "name": tc.name,
            "success": False,
            "expected_success": tc.expected_success,
            "actual_success": False,
            "error": None,
            "expected_error": tc.expected_error,
            "actual_error": "",
            "expected_exception": tc.expected_exception,
            "actual_exception": None,
        }
        driver = self._create_driver()

        try:
            # ── 1. Open login page ──
            print("\n  [1/3] Opening login page...")
            login_page = LoginPage(driver)
            login_page.open_page()
            time.sleep(2)
            print(f"  URL: {login_page.current_url}")
            self._save_screenshot(driver, f"{tc.name}_01_loaded.png")

            # ── 2. Perform login ──
            print("\n  [2/3] Performing login...")
            login_page.login(tc.username, tc.password)
            print(f"  Username: {tc.username or '(empty)'}")
            print(f"  Password:   {'*' * len(tc.password) if tc.password else '(empty)'}")
            self._save_screenshot(driver, f"{tc.name}_02_filled.png")

            # ── 3. Wait for redirect and verify ──
            print("\n  [3/3] Verifying result...")
            time.sleep(3)

            dashboard = DashboardPage(driver)
            actual_success = dashboard.is_dashboard_displayed
            current_url = dashboard.current_url
            print(f"  Current URL: {current_url}")

            result["actual_success"] = actual_success

            # If login fails, check error message
            actual_error_msg = ""
            if not actual_success:
                actual_error_msg = login_page.get_login_error()
                result["actual_error"] = actual_error_msg
                if actual_error_msg:
                    print(f"  Page error message: '{actual_error_msg}'")
                    if tc.expected_error:
                        if tc.expected_error in actual_error_msg:
                            print(f"  ✅ Error message matches: contains '{tc.expected_error}'")
                        else:
                            print(f"  ⚠️ Error message mismatch: expected to contain '{tc.expected_error}'")

            self._save_screenshot(driver, f"{tc.name}_03_result.png")

            # Overall check: login result + error message double verification
            result["success"] = actual_success == tc.expected_success

            # If expected to fail and expected error is set, check additionally
            if not tc.expected_success and tc.expected_error and not actual_success:
                error_match = tc.expected_error in actual_error_msg
                if not error_match:
                    result["success"] = False

        except Exception as e:
            result["error"] = str(e)
            result["actual_exception"] = type(e).__name__
            print(f"\n  ⚠️ Exception: {type(e).__name__}: {e}")
            
            # Check if this was the expected exception
            if tc.expected_exception:
                if isinstance(e, tc.expected_exception):
                    print(f"  ✅ Expected exception occurred: {tc.expected_exception.__name__}")
                    result["success"] = True  # If expected exception occurred, count as success
                else:
                    print(f"  ❌ Unexpected exception type. Expected: {tc.expected_exception.__name__}, Got: {type(e).__name__}")
        finally:
            try:
                driver.quit()
            except:
                pass

        # Print pass/fail
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"\n  >> Result: {status}")
        print(f"     Expected: {'success' if tc.expected_success else 'failure'}")
        print(f"     Actual:   {'success' if result["actual_success"] else 'failure'}")

        return result

    # ── Suite entry point ──────────────────────────────

    def run_suite(self, test_cases: List[TestCase]):
        print("\n" + "=" * 60)
        print("  🏠 fangdong.fun Login Test Suite")
        print(f"  Total test cases: {len(test_cases)}")
        print("=" * 60)

        for i, tc in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}] ", end="")
            result = self._run_test(tc)
            self.results.append(result)

            if i < len(test_cases):
                time.sleep(2)

        self._print_summary()

    # ── Report output ──────────────────────────────

    def _print_summary(self):
        passed = sum(1 for r in self.results if r["success"])
        failed = len(self.results) - passed

        print("\n" + "=" * 60)
        print("  📊 Test Summary")
        print("=" * 60)
        print(f"\n  Total test cases: {len(self.results)}")
        print(f"  Passed:         {passed}")
        print(f"  Failed:         {failed}")
        print()

        for i, r in enumerate(self.results, 1):
            icon = "✅" if r["success"] else "❌"
            print(f"  {icon}  {i:02d}. {r['name']}")
            print(f"       Expected={r['expected_success']}, Actual={r['actual_success']}")
            if r["actual_error"]:
                print(f"       Page message: '{r['actual_error']}'")
            if r["actual_exception"]:
                print(f"       Exception: {r['actual_exception']}")
            if r["error"]:
                print(f"       Error: {r['error'][:80]}...")

        print("\n" + "=" * 60)
        print("  Test completed!" if failed == 0 else f"  {failed} test cases failed")
        print("=" * 60)


# ── Key-value template: test case data ──────────────────────────────

def get_test_cases() -> List[TestCase]:
    return [
        TestCase(
            name="TC001_CorrectCredentials",
            username="testuser3",
            password="123456",
            expected_success=True,
            description="Correct credentials, expect successful redirect",
        ),
        TestCase(
            name="TC002_WrongPassword",
            username="testuser3",
            password="wrongpassword",
            expected_success=False,
            expected_error="用户名或密码错误",
            description="Wrong password, expect to fail with 'username or password wrong error",
        ),
        TestCase(
            name="TC003_NonexistentUsername",
            username="nonexistentuser",
            password="123456",
            expected_success=False,
            expected_error="用户名或密码错误",
            description="Nonexistent username, expect to fail with 'username or password wrong error",
        ),
        TestCase(
            name="TC004_EmptyUsername",
            username="",
            password="123456",
            expected_success=False,
            expected_exception=TimeoutException,
            description="Empty username, expect TimeoutException (element not found or interaction fails)",
        ),
        TestCase(
            name="TC005_EmptyPassword",
            username="testuser3",
            password="",
            expected_success=False,
            expected_exception=TimeoutException,
            description="Empty password, expect TimeoutException (element not found or interaction fails)",
        ),
        TestCase(
            name="TC006_AllEmpty",
            username="",
            password="",
            expected_success=False,
            expected_exception=TimeoutException,
            description="Both username and password empty, expect TimeoutException",
        ),
        TestCase(
            name="TC007_SpecialCharsPassword",
            username="testuser3",
            password="!@#$%^&*()",
            expected_success=False,
            expected_error="用户名或密码错误",
            description="Password contains special characters, expect to fail with username/password error",
        ),
    ]


if __name__ == "__main__":
    LoginTestSuite().run_suite(get_test_cases())
