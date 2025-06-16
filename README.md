# beeMôn Scraper Challenge

Automated data scraping engine built for the beeMôn technical challenge. It supports both command-line execution and scheduled tasks for collecting structured data from various sources.

## Features

- Scrapes from [quotes.toscrape.com](http://quotes.toscrape.com) and IMDb
- Outputs JSON and CSV formats
- Stores data in MongoDB and local files
- Screenshot capture of scraped pages
- Optional email/Telegram notifications
- Dynamic CLI scheduling (`--at`)
- Pandas dataframe summaries
- Fully dockerized and tested (100% coverage)

## Running Tests

poetry run pytest --cov=app --cov-report=term-missing
poetry run coverage-badge -o coverage.svg -f

Coverage
How to Run

# Scrape quotes to JSON
docker compose -f docker/dev.docker-compose.yml run app scrape quotes --format json

# Show IMDB data as table
docker compose -f docker/dev.docker-compose.yml run app show imdb --all

# Schedule quotes scraping
docker compose -f docker/dev.docker-compose.yml run app schedule quotes --at 2025-06-13T08:00

Docker Setup

# Start dev container
docker compose -f docker/dev.docker-compose.yml up

# Production build
docker compose -f docker/prod.docker-compose.yml up --build