"""Simple nav probe - uses the test infrastructure"""
import sys
sys.path.insert(0, '.')
from conftest import retry_on_failure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from helpers import do_login
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,720')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    do_login(driver)
    time.sleep(2)
    
    # Get all elements containing "设置"
    for el in driver.find_elements('xpath', '//*[self::a or self::li or self::span or self::div][contains(text(), "设置")]'):
        tag = el.tag_name
        cls = el.get_attribute('class')
        html_short = el.get_attribute('outerHTML')[:150]
        print(f'<{tag}> class="{cls}" html="{html_short}"')
    
    # Get all sidebar nav items
    print('\n--- All items with el-menu-item or sidebar ---')
    for el in driver.find_elements('xpath', '//*[contains(@class, "menu-item") or contains(@class, "el-menu-item")]'):
        tag = el.tag_name
        text = el.text.strip()
        cls = el.get_attribute('class')
        print(f'<{tag}> class="{cls}" text="{text}"')
    
    # Try getting all elements with href
    print('\n--- All elements with href starting with / ---')
    for el in driver.find_elements('xpath', '//*[@href and starts-with(@href, "/")]'):
        tag = el.tag_name
        text = el.text.strip()
        href = el.get_attribute('href')
        if text:
            print(f'<{tag}> text="{text}" href="{href}"')

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
