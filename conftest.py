import functools
import time
import signal
import datetime
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# 存储测试结果和日志
_test_logs = {}
_current_test = None
_screenshot_dir = "test_screenshots"


def pytest_runtest_setup(item):
    """测试setup阶段"""
    global _current_test
    _current_test = item.name
    _test_logs[_current_test] = {
        "start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "end_time": None,
        "duration": None,
        "status": "SETUP",
        "logs": [],
        "screenshots": []
    }
    print(f"\n[SETUP] {_current_test} started at {_test_logs[_current_test]['start_time']}")


def pytest_runtest_teardown(item, nextitem):
    """测试teardown阶段"""
    global _current_test
    if _current_test and _current_test in _test_logs:
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        _test_logs[_current_test]["end_time"] = end_time
        
        # 计算耗时
        start = datetime.datetime.strptime(_test_logs[_current_test]["start_time"], "%Y-%m-%d %H:%M:%S.%f")
        end = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
        _test_logs[_current_test]["duration"] = str(end - start)
        
        print(f"[TEARDOWN] {_current_test} finished at {end_time}")


def pytest_runtest_logreport(report):
    """实时捕获测试结果"""
    global _current_test
    if report.when == "call":
        if _current_test and _current_test in _test_logs:
            if report.passed:
                _test_logs[_current_test]["status"] = "PASS"
            elif report.failed:
                _test_logs[_current_test]["status"] = "FAIL"
                # 捕获失败原因
                if hasattr(report, 'longrepr'):
                    _test_logs[_current_test]["error"] = str(report.longrepr)
            elif report.skipped:
                _test_logs[_current_test]["status"] = "SKIP"


@pytest.fixture
def test_logger(request):
    """测试日志fixture - 供测试用例记录执行步骤"""
    global _current_test
    return TestLogger(_current_test)


class TestLogger:
    """测试日志记录器"""
    def __init__(self, test_name):
        self.test_name = test_name
        self._logs = []
    
    def log(self, message):
        """记录执行步骤"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}"
        self._logs.append(log_entry)
        print(f"  {log_entry}")
        if self.test_name and self.test_name in _test_logs:
            _test_logs[self.test_name]["logs"].append(log_entry)
    
    def screenshot(self, step_name):
        """记录截屏"""
        if self.test_name and self.test_name in _test_logs:
            _test_logs[self.test_name]["screenshots"].append(step_name)


def pytest_sessionfinish(session, exitstatus):
    """所有测试执行完毕后生成HTML报告"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成详细HTML报告
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Report - {timestamp}</title>
    <style>
        body {{ font-family: 'Consolas', 'Courier New', monospace; margin: 20px; background: #1e1e1e; color: #d4d4d4; }}
        h1 {{ color: #569cd6; border-bottom: 2px solid #569cd6; padding-bottom: 10px; }}
        .summary {{ background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary .timestamp {{ color: #608b4e; }}
        .summary .stats {{ margin-top: 10px; }}
        .pass {{ color: #4ec9b0; }} .fail {{ color: #f14c4c; }} .skip {{ color: #dcdcaa; }}
        .test-case {{ background: #2d2d2d; margin: 15px 0; border-radius: 8px; border-left: 4px solid #569cd6; }}
        .test-case.pass {{ border-left-color: #4ec9b0; }}
        .test-case.fail {{ border-left-color: #f14c4c; }}
        .case-header {{ padding: 15px; cursor: pointer; }}
        .case-header:hover {{ background: #3c3c3c; }}
        .case-name {{ font-size: 16px; font-weight: bold; color: #569cd6; }}
        .case-time {{ font-size: 12px; color: #808080; margin-top: 5px; }}
        .case-content {{ display: none; padding: 15px; border-top: 1px solid #3c3c3c; }}
        .case-content.show {{ display: block; }}
        .log-entry {{ padding: 5px 0; border-bottom: 1px solid #3c3c3c; }}
        .log-time {{ color: #608b4e; }}
        .screenshot {{ margin: 10px 0; }}
        .screenshot img {{ max-width: 400px; border: 2px solid #3c3c3c; border-radius: 4px; }}
        .screenshot-label {{ color: #808080; font-size: 12px; margin-top: 5px; }}
        .error {{ background: #3c1e1e; padding: 10px; border-radius: 4px; color: #f14c4c; margin-top: 10px; }}
        th {{ background: #0e639c !important; color: white !important; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #3c3c3c; padding: 10px; text-align: left; }}
    </style>
    <script>
        function toggleCase(id) {{
            var content = document.getElementById(id);
            content.classList.toggle('show');
        }}
    </script>
</head>
<body>
    <h1>Test Report</h1>
    <div class="summary">
        <p><strong>Report Time:</strong> <span class="timestamp">{timestamp}</span></p>
        <div class="stats">
"""
    
    passed = sum(1 for r in _test_logs.values() if r["status"] == "PASS")
    failed = sum(1 for r in _test_logs.values() if r["status"] == "FAIL")
    skipped = sum(1 for r in _test_logs.values() if r["status"] == "SKIP")
    total = len(_test_logs)
    
    html += f"""            <span class="pass">PASS: {passed}</span> | 
            <span class="fail">FAIL: {failed}</span> | 
            <span class="skip">SKIP: {skipped}</span> | 
            <span>Total: {total}</span>
        </div>
    </div>
    <h2>Test Cases</h2>
"""
    
    for name, data in _test_logs.items():
        status_class = data["status"].lower()
        case_id = name.replace("[", "_").replace("]", "_").replace(" ", "_")
        
        html += f"""    <div class="test-case {status_class}">
        <div class="case-header" onclick="toggleCase('{case_id}')">
            <div class="case-name">{data['status']} - {name}</div>
            <div class="case-time">Start: {data['start_time']} | End: {data['end_time']} | Duration: {data['duration']}</div>
        </div>
        <div class="case-content" id="{case_id}">
"""
        
        # 执行步骤日志
        if data["logs"]:
            html += "            <h4>Execution Logs:</h4>\n"
            for log in data["logs"]:
                html += f'            <div class="log-entry"><span class="log-time">{log}</span></div>\n'
        
        # 截屏
        if data["screenshots"]:
            html += "            <h4>Screenshots:</h4>\n"
            for i, shot in enumerate(data["screenshots"], 1):
                img_path = f"{_screenshot_dir}/{name}_{shot}.png"
                if os.path.exists(img_path):
                    html += f"""            <div class="screenshot">
                <div class="screenshot-label">{shot}</div>
                <img src="{img_path}" alt="{shot}">
            </div>
"""
        
        # 错误信息
        if data.get("error"):
            html += f'            <div class="error">Error: {data["error"]}</div>\n'
        
        html += "        </div>\n    </div>\n"
    
    html += """</body>
</html>"""
    
    with open("test_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n[Test Report] test_report.html generated at {timestamp}")


def retry_on_failure(max_retries=1, delay=1):
    """Decorator: automatically retry test function on exception, with 3s delay between retries.
    
    Usage:
        @retry_on_failure(max_retries=3, delay=3)
        def test_something():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_retries:
                        print(f"\n  ⚠️ Attempt {attempt} failed: {type(e).__name__}: {e}")
                        print(f"  🔄 Retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                    else:
                        print(f"\n  ❌ All {max_retries} attempts failed.")
                        raise last_exc
            return None
        return wrapper
    return decorator


@pytest.fixture(scope="function")
def driver():
    """Fixture: create Chrome driver per test function, auto-quit after each test."""
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    try:
        driver.quit()
    except:
        pass


@pytest.fixture(scope="class")
def class_driver():
    """Fixture: create Chrome driver per test class, auto-quit after all tests."""
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    try:
        driver.quit()
    except:
        pass
