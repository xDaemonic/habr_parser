import time, datetime
start = datetime.datetime.now()

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless=new')
options.add_argument('--start-maximized')
options.add_argument('--disable-javascript')
# options.add_argument('--remote-debugging-port=9222')

prefs = {}
prefs["webkit.webprefs.javascript_enabled"] = False
prefs["profile.content_settings.exceptions.javascript.*.setting"] = 2
prefs["profile.default_content_setting_values.javascript"] = 2
prefs["profile.managed_default_content_settings.javascript"] = 2
options.add_experimental_option( "prefs",prefs)

driver = webdriver.Chrome(options=options)

def test_fullpage_screenshot(driver, url: str, filename: str):
    try:
        # driver.execute_cdp_cmd("Network.setBlockedURLs", {
        #     "urls": ["*.js"]
        # })
        driver.get(url)

        height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, height)

        driver.save_screenshot(f"screenshots/{filename}")
    except Exception:
        print(Exception)
        pass
        
if __name__ == "__main__":
    url = "https://freelance.habr.com/tasks?categories=development_all_inclusive%2Cdevelopment_backend%2Cdevelopment_frontend%2Cdevelopment_prototyping%2Cdevelopment_ios%2Cdevelopment_android%2Cdevelopment_desktop%2Cdevelopment_bots%2Cdevelopment_games%2Cdevelopment_1c_dev%2Cdevelopment_scripts%2Cdevelopment_voice_interfaces%2Cdevelopment_other"
    cnt = 0
    
    while (cnt  < 4):
        filename = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ".png"
        print(f"getting file {filename}")
        test_fullpage_screenshot(driver, url, filename)
        print(f"getting end {filename}")
        cnt += 1

    end = datetime.datetime.now()
    delta = end - start
    driver.quit()
    print(f"script works: {delta}")