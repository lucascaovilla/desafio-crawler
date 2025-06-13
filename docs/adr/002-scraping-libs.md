# ADR 002: Use BeautifulSoup + Requests for scraping

## Context
Scrapy is powerful but can be overkill for basic structured pages. Selenium is needed only for dynamic content (e.g., screenshot).

## Decision
Use `requests` + `BeautifulSoup` for scraping, and `Selenium` for screenshots only.

## Alternatives
- Scrapy: too heavyweight
- Selenium-only: too slow for scraping large pages

## Consequences
- Faster development, simple structure
