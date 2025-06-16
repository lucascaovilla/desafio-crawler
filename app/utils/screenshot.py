import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(site: str):
    os.makedirs("screenshots", exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{site}_{timestamp}.png"
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    if site == "quotes":
        driver.get("http://quotes.toscrape.com")
    elif site == "imdb":
        driver.get("https://www.imdb.com/chart/top")

    driver.save_screenshot(filename)
    driver.quit()
    print(f"Screenshot saved: {filename}")
