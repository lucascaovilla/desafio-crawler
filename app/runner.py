import os
import datetime
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

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        if fmt == "json":
            os.makedirs("data/json", exist_ok=True)
            file.save_as_json(data, output or f"data/json/{site}_{timestamp}.json")
        elif fmt == "csv":
            os.makedirs("data/csv", exist_ok=True)
            file.save_as_csv(data, output or f"data/csv/{site}_{timestamp}.csv")
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

        if args.all:
            pd.set_option("display.max_rows", None)
            pd.set_option("display.max_colwidth", None)
            pd.set_option("display.width", None)
            print(df.head(len(df)))
        else:
            print(df.head())

        logger.info(f"Displayed data for site: {args.site}")
    except Exception as e:
        logger.exception("Failed to show data")
