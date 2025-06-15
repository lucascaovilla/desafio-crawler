from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from app.logger import get_logger

URL = "https://www.imdb.com/chart/top"
logger = get_logger(__name__)

def scrape():
    logger.info("Starting IMDb scraping")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(URL)

        movies = []
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody.lister-list tr")
        for row in rows[:10]:
            title = row.find_element(By.CSS_SELECTOR, "td.titleColumn a").text
            year = row.find_element(By.CSS_SELECTOR, "td.titleColumn span").text.strip("()")
            rating = row.find_element(By.CSS_SELECTOR, "td.ratingColumn.imdbRating").text.strip()
            movies.append({"title": title, "year": year, "rating": rating})

        logger.info(f"Scraped {len(movies)} IMDb movies")
        return movies

    except Exception:
        logger.exception("IMDb scraping failed")
        raise
    finally:
        driver.quit()
