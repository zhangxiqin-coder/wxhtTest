"""Simple nav dump - uses test helper directly"""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from helpers import do_login

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

    # Dump the sidebar HTML structure
    sidebars = driver.find_elements('xpath', '//*[contains(@class, "sidebar") or contains(@class, "el-menu")]')
    print(f"Sidebar elements found: {len(sidebars)}")
    for sb in sidebars:
        print("--- Sidebar HTML ---")
        print(sb.get_attribute('outerHTML')[:2000])
    
    # Also look for any element containing "设置"
    print("\n--- Elements containing 设置 ---")
    for el in driver.find_elements('xpath', '//*[contains(text(), "设置")]'):
        tag = el.tag_name
        cls = el.get_attribute('class')
        outer = el.get_attribute('outerHTML')[:200]
        aria_label = el.get_attribute('aria-label')
        role = el.get_attribute('role')
        print(f'<{tag}> class="{cls}" role="{role}" aria-label="{aria_label}"')
        print(f'  HTML: {outer}')
        print()

except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
