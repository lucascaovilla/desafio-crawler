# beeMôn Scraper Challenge

Automated data scraping engine built for the beeMôn technical challenge. It supports both command-line execution and scheduled tasks for collecting structured data from various sources.

## Features

- Scrapes from [quotes.toscrape.com](http://quotes.toscrape.com) and IMDb
- Outputs JSON and CSV formats
- Stores data in MongoDB and local files
- Screenshot capture of scraped pages
- Optional email/Telegram notifications
- Dynamic CLI scheduling (`--at`) with email notification (`--notify-to`)
- Pandas dataframe summaries
- Fully dockerized and tested

## Running Tests

docker compose -f docker/test.docker-compose.yml run test pytest --cov=app --cov-report=term-missing

### Generating Test Coverage Badge

docker compose -f docker/test.docker-compose.yml run test coverage-badge -o coverage.svg -f


![Coverage](coverage.svg)


# How to Run

## Dev

### Scrape quotes to JSON
docker compose -f docker/dev.docker-compose.yml run dev scrape quotes --format json

### Show IMDB data as table
docker compose -f docker/dev.docker-compose.yml run dev show imdb --all

### Schedule quotes scraping
docker compose -f docker/dev.docker-compose.yml run dev schedule quotes --at 2025-06-13T08:00 --notify-to your@email.example

## Prod

### Scrape quotes to JSON
docker compose -f docker/prod.docker-compose.yml run prod scrape quotes --format json

### Show IMDB data as table
docker compose -f docker/prod.docker-compose.yml run prod show imdb --all

### Schedule quotes scraping
docker compose -f docker/prod.docker-compose.yml run prod schedule quotes --at 2025-06-13T08:00 --notify-to your@email.example