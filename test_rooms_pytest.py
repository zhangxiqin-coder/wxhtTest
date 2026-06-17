"""Test rooms page - room table, actions, pagination"""
import time
import pytest
from pages.rooms_page import RoomsPage
from conftest import retry_on_failure
from helpers import do_login


@retry_on_failure(max_retries=1, delay=2)
def test_rooms_page_loads(driver):
    """Rooms page should load after login"""
    do_login(driver)
    rooms = RoomsPage(driver)
    rooms.open_page()
    time.sleep(2)
    
    assert rooms.is_on_rooms_page, f"Expected /rooms, got {driver.current_url}"


@retry_on_failure(max_retries=1, delay=2)
def test_add_room_button_visible(driver):
    """Add room button should be displayed"""
    do_login(driver)
    rooms = RoomsPage(driver)
    rooms.open_page()
    time.sleep(1)
    
    assert rooms.add_room_btn.is_displayed(), "Add room button not visible"


@retry_on_failure(max_retries=1, delay=2)
def test_batch_import_button_visible(driver):
    """Batch import button should be displayed"""
    do_login(driver)
    rooms = RoomsPage(driver)
    rooms.open_page()
    time.sleep(1)
    
    assert rooms.batch_import_btn.is_displayed(), "Batch import button not visible"


@retry_on_failure(max_retries=1, delay=2)
def test_room_table_has_data(driver):
    """Room table should have room count displayed"""
    do_login(driver)
    rooms = RoomsPage(driver)
    rooms.open_page()
    time.sleep(1)
    
    count = rooms.get_room_count()
    print(f"  Room count: {count}")
    assert count > 0, f"Expected rooms > 0, got {count}"


@retry_on_failure(max_retries=1, delay=2)
def test_room_rows_exist(driver):
    """Room table should contain at least one row"""
    do_login(driver)
    rooms = RoomsPage(driver)
    rooms.open_page()
    time.sleep(1)
    
    rows = driver.find_elements("xpath", "//tr[contains(@class, 'el-table__row')]")
    print(f"  Room rows found: {len(rows)}")
    assert len(rows) > 0, "No room rows found in table"
