from app.scrapers import quotes_scraper, imdb_scraper
from app.storage import file, db
from app.utils.screenshot import take_screenshot
from app.logger import get_logger
import pandas as pd

logger = get_logger(__name__)

def run_scraper(args):
    site = args.site
    fmt = args.format
    output = args.output

    logger.info(f"Scraping site: {site}")
    
    try:
        if site == "quotes":
            data = quotes_scraper.scrape()
        elif site == "imdb":
            data = imdb_scraper.scrape()
        else:
            raise ValueError("Unknown site")

        logger.info(f"Scraped {len(data)} items from {site}")

        if fmt == "json":
            file.save_as_json(data, output or f"{site}.json")
        elif fmt == "csv":
            file.save_as_csv(data, output or f"{site}.csv")
        logger.info(f"Saved data in {fmt.upper()} format")

        if not getattr(args, "no_screenshot", False):
            take_screenshot(site)

        db.store_data(site, data)
        logger.info(f"Data stored in DB for {site}")

    except Exception as e:
        logger.exception("Failed to run scraper")

def show_data(args):
    try:
        data = db.fetch_all(args.site)
        df = pd.DataFrame(data)
        print(df.head())
        logger.info(f"Displayed data for site: {args.site}")
    except Exception as e:
        logger.exception("Failed to show data")
