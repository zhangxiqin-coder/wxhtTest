"""Test rooms page - room table, actions, pagination"""
import time
import pytest
from pages.rooms_page import RoomsPage
from pages.login_page import LoginPage
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


class TestRoomsSuite:
    """房间管理测试套件"""

    @pytest.fixture(autouse=True)
    def _setup_driver(self, suite_login, test_logger):
        """自动注入suite_login和logger fixture"""
        self.driver = suite_login
        self.test_logger = test_logger
        yield suite_login

    def test_rooms_page_loads(self):
        """Rooms page should load after login"""
        self.test_logger.log("=== Starting test: test_rooms_page_loads ===")
        rooms = RoomsPage(self.driver)
        rooms.open_page()
        self.test_logger.log(f"Rooms page loaded: {self.driver.current_url}")
        
        assert rooms.is_on_rooms_page, f"Expected /rooms, got {self.driver.current_url}"
        self.test_logger.log("PASS: Rooms page loaded successfully")

    def test_add_room_button_visible(self):
        """Add room button should be displayed"""
        self.test_logger.log("=== Starting test: test_add_room_button_visible ===")
        rooms = RoomsPage(self.driver)
        rooms.open_page()
        self.test_logger.log("Rooms page opened")
        
        assert rooms.add_room_btn.is_displayed(), "Add room button not visible"
        self.test_logger.log("PASS: Add room button is visible")

    def test_batch_import_button_visible(self):
        """Batch import button should be displayed"""
        self.test_logger.log("=== Starting test: test_batch_import_button_visible ===")
        rooms = RoomsPage(self.driver)
        rooms.open_page()
        self.test_logger.log("Rooms page opened")
        
        assert rooms.batch_import_btn.is_displayed(), "Batch import button not visible"
        self.test_logger.log("PASS: Batch import button is visible")

    def test_room_table_has_data(self):
        """Room table should have room count displayed"""
        self.test_logger.log("=== Starting test: test_room_table_has_data ===")
        rooms = RoomsPage(self.driver)
        rooms.open_page()
        self.test_logger.log("Rooms page opened")
        
        count = rooms.get_room_count()
        self.test_logger.log(f"Room count: {count}")
        assert count > 0, f"Expected rooms > 0, got {count}"
        self.test_logger.log("PASS: Room table has data")

    def test_room_rows_exist(self):
        """Room table should contain at least one row"""
        self.test_logger.log("=== Starting test: test_room_rows_exist ===")
        rooms = RoomsPage(self.driver)
        rooms.open_page()
        self.test_logger.log("Rooms page opened")
        # wait for room table to load data
        time.sleep(2)
        rows = self.driver.find_elements("xpath", "//tr[contains(@class, 'el-table__row')]")
        self.test_logger.log(f"Room rows found: {len(rows)}")
        assert len(rows) > 0, "No room rows found in table"
        self.test_logger.log("PASS: Room rows exist")
