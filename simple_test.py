from selenium import webdriver
import time

print("正在启动浏览器...")
driver = webdriver.Chrome()

try:
    print("正在打开网页...")
    driver.get("https://fangdong.fun/")
    print("网页已打开!")
    print("页面标题:", driver.title)
    print("当前URL:", driver.current_url)
    
    time.sleep(3)
    
    print("测试完成!")
    
except Exception as e:
    print(f"错误: {e}")
finally:
    time.sleep(2)
    driver.quit()
    print("浏览器已关闭")
