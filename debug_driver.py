from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys
import time

print("=== 调试 ChromeDriver ===")
print(f"Python 版本: {sys.version}")

try:
    import selenium
    print(f"Selenium 版本: {selenium.__version__}")
except ImportError:
    print("Selenium 未安装")

print("\n尝试启动浏览器...")

options = Options()
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

try:
    print("方法1: 使用默认 ChromeDriver...")
    driver = webdriver.Chrome(options=options)
    print("✓ 方法1成功!")
    driver.quit()
    
except Exception as e:
    print(f"✗ 方法1失败: {type(e).__name__}: {e}")
    
    print("\n尝试使用 Service 对象...")
    try:
        from selenium.webdriver.chrome.service import Service
        driver = webdriver.Chrome(service=Service(), options=options)
        print("✓ Service 方法成功!")
        driver.quit()
    except Exception as e2:
        print(f"✗ Service 方法也失败: {e2}")
        
        print("\n尝试使用 webdriver-manager...")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print("✓ webdriver-manager 成功!")
            driver.quit()
        except ImportError:
            print("需要安装 webdriver-manager")
            print("请运行: pip install webdriver-manager")
        except Exception as e3:
            print(f"✗ webdriver-manager 失败: {e3}")

print("\n=== 调试完成 ===")
