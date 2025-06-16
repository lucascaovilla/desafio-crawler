import requests
from bs4 import BeautifulSoup
import time
import random
from app.logger import get_logger

logger = get_logger(__name__)

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        time.sleep(random.uniform(1, 3))

        response = session.get('https://www.imdb.com/chart/top', timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        movies = []

        rows = soup.select('li.ipc-metadata-list-summary-item')

        for row in rows:
            try:
                title_tag = row.select_one('h3.ipc-title__text')
                year_tag = row.select_one('.cli-title-metadata span')
                rating_tag = row.select_one('[data-testid="ratingGroup--imdb-rating"] span.ipc-rating-star--rating')

                if title_tag and year_tag and rating_tag:
                    title = title_tag.get_text(strip=True)
                    year = year_tag.get_text(strip=True)
                    rating = rating_tag.get_text(strip=True)

                    movies.append({
                        "title": title,
                        "year": year,
                        "rating": rating
                    })
                else:
                    logger.debug(f"Missing data in one row: title={title_tag}, year={year_tag}, rating={rating_tag}")

            except Exception as e:
                logger.warning(f"Failed to parse movie row: {e}")
                continue

        logger.info(f"Scraped {len(movies)} IMDb movies")
        return movies

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise
    except Exception as e:
        logger.exception("IMDb scraping failed")
        raise
    finally:
        session.close()
