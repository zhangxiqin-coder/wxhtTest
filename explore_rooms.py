"""Explore rooms page elements in detail"""
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
    # Login first
    login = LoginPage(driver)
    login.open_page()
    time.sleep(2)
    login.login('testuser3', '123456')
    time.sleep(3)

    # On rooms page already after login, but navigate explicitly
    driver.get('https://fangdong.fun/rooms')
    time.sleep(2)
    print('Rooms URL:', driver.current_url)
    print('Rooms title:', driver.title)

    # Get all elements with significant attributes
    for el in driver.find_elements('xpath', '//*[not(self::script) and not(self::style)]'):
        tag = el.tag_name
        text = el.text.strip()
        _id = el.get_attribute('id')
        cls = el.get_attribute('class')
        placeholder = el.get_attribute('placeholder')
        type_attr = el.get_attribute('type')
        name_attr = el.get_attribute('name')
        
        if _id or placeholder or name_attr or (text and len(text) < 50):
            print(f'  <{tag}> id={_id} class={cls} text="{text}" placeholder={placeholder} type={type_attr} name={name_attr}')

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
