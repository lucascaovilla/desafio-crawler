import requests
from bs4 import BeautifulSoup
from app.logger import get_logger

URL = "http://quotes.toscrape.com"
logger = get_logger(__name__)

def scrape():
    logger.info("Starting quotes.toscrape scraping")
    try:
        res = requests.get(URL)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = []

        for quote in soup.select(".quote"):
            text = quote.select_one(".text").get_text(strip=True)
            author = quote.select_one(".author").get_text(strip=True)
            quotes.append({"text": text, "author": author})

        logger.info(f"Scraped {len(quotes)} quotes")
        return quotes
    except Exception:
        logger.exception("Quotes scraping failed")
        raise
