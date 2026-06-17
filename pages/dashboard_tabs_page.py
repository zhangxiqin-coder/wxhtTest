from pages.base_page import BasePage


class DashboardTabsPage(BasePage):
    """Dashboard page containing tab-based sub-pages: Rooms, Tenants, Payments, Utility.

    All four sections are tabs under the same URL (/rooms), and do not require 
    separate page navigation - just click the tab header to switch content.
    """

    url = "https://fangdong.fun/rooms"

    @property
    def is_on_dashboard(self):
        """Check if successfully on the dashboard (any tab)"""
        return "/rooms" in self.current_url

    def open_page(self):
        """Open the rooms dashboard page directly"""
        self.open(self.url)
