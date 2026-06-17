"""Quick script to explore website pages after login"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,720')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Login first
    login = LoginPage(driver)
    login.open_page()
    time.sleep(2)
    login.login('testuser3', '123456')
    time.sleep(3)

    print('After login URL:', driver.current_url)
    print('Page title:', driver.title)

    # Get all clickable elements (links and buttons)
    all_links = driver.find_elements('xpath', '//a | //button')
    print(f'\nTotal clickable elements found: {len(all_links)}')
    for el in all_links:
        href = el.get_attribute('href')
        text = el.text.strip()
        onclick = el.get_attribute('onclick')
        tag = el.tag_name
        if text:
            print(f'  <{tag}> [{text}] href={href} onclick={onclick}')

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
