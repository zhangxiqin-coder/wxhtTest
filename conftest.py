import functools
import time
import signal

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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
