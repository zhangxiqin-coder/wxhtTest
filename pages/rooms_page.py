from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class RoomsPage(BasePage):
    """Room management page PO - shows room table with actions"""

    # ── Room page actions ──
    add_room_btn = FindBy(By.XPATH, "//button[contains(., '添加房间')]")
    batch_import_btn = FindBy(By.XPATH, "//button[contains(., '批量导入')]")

    # Room table columns (header)
    table_headers = FindBy(By.XPATH, "//div[contains(@class, 'el-table__header')]//th")

    # Room table rows (data rows)
    room_rows = FindBy(By.XPATH, "//tr[contains(@class, 'el-table__row')]")

    # Pagination
    total_label = FindBy(By.CLASS_NAME, "el-pagination__total")

    def open_page(self):
        """Open rooms page"""
        self.open("https://fangdong.fun/rooms")

    @property
    def is_on_rooms_page(self):
        return "/rooms" in self.current_url

    def get_room_count(self) -> int:
        """Get total room count from pagination label"""
        try:
            text = self.total_label.text
            # Format: "Total 5"
            return int(text.replace("Total ", ""))
        except:
            return 0

    def get_all_rooms(self) -> list[dict]:
        """Extract room data from the table rows"""
        # This would require iterating table cells - simplified for now
        pass
