import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def test_fullpage_screenshot(url: str, filename: str):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(2)

        ele = driver.find_element(By.TAG_NAME, 'body')
        height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, height)

        driver.save_screenshot(f"screenshots/{filename}")
    except Exception:
        pass
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    test_fullpage_screenshot("https://vk.com/", "vk.png")
