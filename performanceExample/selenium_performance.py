"""
Selenium 性能测试示例

用于测试页面加载时间和前端性能
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def measure_page_load_time(url: str, iterations: int = 3) -> float:
    """
    测量页面加载时间
    
    Args:
        url: 要测试的页面URL
        iterations: 测试次数
    
    Returns:
        平均加载时间（秒）
    """
    # 配置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 无头模式
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-images")  # 禁用图片加载（可选）
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        total_time = 0
        
        for i in range(iterations):
            # 导航到页面并记录时间
            start = time.time()
            driver.get(url)
            
            # 等待页面完全加载
            driver.execute_script("return document.readyState") == "complete"
            
            elapsed = time.time() - start
            total_time += elapsed
            print(f"Iteration {i+1}: {elapsed:.4f}s")
        
        avg_time = total_time / iterations
        print(f"\nAverage page load time: {avg_time:.4f}s")
        
        return avg_time
    
    finally:
        driver.quit()


def measure_login_performance(username: str, password: str) -> float:
    """
    测量登录流程的性能
    
    Args:
        username: 用户名
        password: 密码
    
    Returns:
        登录完成时间（秒）
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        start = time.time()
        
        # 打开登录页面
        driver.get("https://fangdong.fun/login")
        
        # 输入用户名
        username_input = driver.find_element("xpath", "//input[@type='text']")
        username_input.send_keys(username)
        
        # 输入密码
        password_input = driver.find_element("xpath", "//input[@type='password']")
        password_input.send_keys(password)
        
        # 点击登录按钮
        login_button = driver.find_element("xpath", "//button[contains(text(), '登录')]")
        login_button.click()
        
        # 等待页面跳转
        time.sleep(2)
        
        elapsed = time.time() - start
        print(f"Login performance: {elapsed:.4f}s")
        
        return elapsed
    
    finally:
        driver.quit()


def analyze_performance_timing(driver) -> dict:
    """
    分析页面性能计时数据
    
    Args:
        driver: Selenium WebDriver 实例
    
    Returns:
        性能计时数据字典
    """
    timing = driver.execute_script("return window.performance.timing")
    
    metrics = {
        "navigation_time": timing["navigationStart"],
        "unload_event_start": timing["unloadEventStart"],
        "unload_event_end": timing["unloadEventEnd"],
        "redirect_start": timing["redirectStart"],
        "redirect_end": timing["redirectEnd"],
        "fetch_start": timing["fetchStart"],
        "domain_lookup_start": timing["domainLookupStart"],
        "domain_lookup_end": timing["domainLookupEnd"],
        "connect_start": timing["connectStart"],
        "connect_end": timing["connectEnd"],
        "secure_connection_start": timing["secureConnectionStart"],
        "request_start": timing["requestStart"],
        "response_start": timing["responseStart"],
        "response_end": timing["responseEnd"],
        "dom_loading": timing["domLoading"],
        "dom_interactive": timing["domInteractive"],
        "dom_content_loaded_event_start": timing["domContentLoadedEventStart"],
        "dom_content_loaded_event_end": timing["domContentLoadedEventEnd"],
        "dom_complete": timing["domComplete"],
        "load_event_start": timing["loadEventStart"],
        "load_event_end": timing["loadEventEnd"],
    }
    
    # 计算关键指标
    metrics["total_load_time"] = (metrics["load_event_end"] - metrics["navigation_time"]) / 1000
    metrics["dom_interactive_time"] = (metrics["dom_interactive"] - metrics["navigation_time"]) / 1000
    metrics["first_contentful_paint"] = (metrics["response_end"] - metrics["navigation_time"]) / 1000
    
    return metrics


if __name__ == "__main__":
    print("=" * 60)
    print("Selenium 性能测试示例")
    print("=" * 60)
    
    # 测试页面加载时间
    print("\n1. 测试页面加载时间:")
    measure_page_load_time("https://fangdong.fun/login", iterations=3)
    
    # 测试登录性能
    print("\n2. 测试登录性能:")
    measure_login_performance("testuser3", "123456")
    
    print("\n" + "=" * 60)
    print("性能测试完成")
    print("=" * 60)
