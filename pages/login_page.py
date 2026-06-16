from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.element import FindBy


class LoginPage(BasePage):
    """Login page PO"""

    # ── Page element declarations (@FindBy descriptor style) ──
    username_input = FindBy(By.XPATH, "//input[@type='text']")
    password_input = FindBy(By.XPATH, "//input[@type='password']")
    login_button = FindBy(By.XPATH, "//button[contains(text(),'登录')]")
    register_link = FindBy(By.XPATH, "//a[contains(text(),'去注册')]")
    form_error = FindBy(By.XPATH, "//div[contains(@class,'form-error')]")

    # Page URL
    url = "https://fangdong.fun/"

    def open_page(self):
        """Open login page"""
        self.open(self.url)

    def login(self, username: str, password: str):
        """Perform login operation"""
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.login_button.click()

    def get_login_error(self) -> str:
        """Get login error message text"""
        try:
            return self.form_error.text
        except:
            return ""

    @property
    def has_login_error(self) -> bool:
        """Check if login error is displayed on page"""
        try:
            return self.form_error.is_displayed()
        except:
            return False

    @property
    def is_on_login_page(self):
        """Check if currently on login page"""
        return "login" in self.current_url.lower()
