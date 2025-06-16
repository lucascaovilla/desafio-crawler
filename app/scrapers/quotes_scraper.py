import requests
from bs4 import BeautifulSoup
from app.logger import get_logger

URL = "http://quotes.toscrape.com"
logger = get_logger(__name__)

def scrape():
    logger.info("Starting quotes.toscrape scraping with pagination")
    quotes = []
    page = 1
    
    try:
        while True:
            if page == 1:
                current_url = URL
            else:
                current_url = f"{URL}/page/{page}/"
            
            logger.info(f"Scraping page {page}: {current_url}")
            
            res = requests.get(current_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            
            page_quotes = soup.select(".quote")
            
            if not page_quotes:
                logger.info(f"No quotes found on page {page}, stopping pagination")
                break
            
            for quote in page_quotes:
                text = quote.select_one(".text").get_text(strip=True)
                author = quote.select_one(".author").get_text(strip=True)
                
                tag_elements = quote.select(".tags .tag")
                tags = [tag.get_text(strip=True) for tag in tag_elements]
                
                quotes.append({
                    "text": text,
                    "author": author,
                    "tags": tags
                })
            
            logger.info(f"Scraped {len(page_quotes)} quotes from page {page}")
            
            next_btn = soup.select_one(".pager .next")
            if not next_btn:
                logger.info("No 'Next' button found, reached last page")
                break
            
            page += 1

        logger.info(f"Scraping completed. Total quotes scraped: {len(quotes)}")
        return quotes
        
    except Exception:
        logger.exception("Quotes scraping failed")
        raise