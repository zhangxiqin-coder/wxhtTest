"""诊断脚本：登录失败后页面的错误提示元素"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,720')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://fangdong.fun/")
    time.sleep(2)

    # 用错误密码登录
    username = driver.find_element(By.XPATH, "//input[@type='text']")
    password = driver.find_element(By.XPATH, "//input[@type='password']")
    username.send_keys("testuser3")
    password.send_keys("wrongpassword")

    btn = driver.find_element(By.XPATH, "//button[contains(text(),'登录')]")
    btn.click()
    time.sleep(3)

    print("=== 登录失败后页面源码（相关片段）===")
    source = driver.page_source
    # 查找包含错误/提示信息的关键区域
    for keyword in ["错误", "error", "msg", "提示", "用户名", "密码", "alert", "danger", "message", "toast"]:
        idx = source.lower().find(keyword.lower())
        if idx > 0:
            start = max(0, idx - 100)
            end = min(len(source), idx + 200)
            print(f"\n--- 关键词 '{keyword}' 附近 ---")
            print(source[start:end])

    print("\n=== 查找常见错误元素 ===")
    selectors = [
        "//div[contains(@class,'error')]",
        "//div[contains(@class,'alert')]",
        "//div[contains(@class,'message')]",
        "//div[contains(@class,'toast')]",
        "//span[contains(@class,'error')]",
        "//p[contains(@class,'error')]",
        "//div[contains(@class,'el-message')]",
        "//div[contains(@role,'alert')]",
        "//div[contains(@class,'notification')]",
        "//div[contains(@class,'tip')]",
    ]
    for sel in selectors:
        try:
            el = driver.find_elements(By.XPATH, sel)
            if el:
                for e in el:
                    print(f"  {sel}: text='{e.text[:100]}' display={e.is_displayed()}")
        except:
            pass

    print("\n=== 所有可见提示文本 ===")
    body = driver.find_element(By.TAG_NAME, "body")
    all_text = body.text
    for line in all_text.split("\n"):
        if line.strip():
            print(f"  '{line.strip()}'")

except Exception as e:
    print(f"错误: {e}")
finally:
    driver.quit()
