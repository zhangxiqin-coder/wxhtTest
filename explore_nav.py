"""Find exact settings link locator"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,720')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    login = LoginPage(driver)
    login.open_page()
    time.sleep(2)
    login.login('testuser3', '123456')
    time.sleep(3)

    # Find the settings link specifically
    for el in driver.find_elements('xpath', '//*[contains(text(), "设置")]'):
        tag = el.tag_name
        html = el.get_attribute('outerHTML')
        print(f'<{tag}> outerHTML: {html[:200]}')

    print('\n--- All sidebar links (li/el-menu-item) ---')
    for el in driver.find_elements('xpath', '//li | //*[contains(@class, "menu")]//a | //*[contains(@class, "menu")]//span'):
        tag = el.tag_name
        text = el.text.strip()
        cls = el.get_attribute('class')
        href = el.get_attribute('href')
        if text:
            print(f'  <{tag}> class="{cls}" text="{text}" href="{href}"')

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
