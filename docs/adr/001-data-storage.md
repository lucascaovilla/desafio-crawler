# ADR 001: Choice of MongoDB for Data Storage

## Context
Scraped data is semi-structured and varies slightly between websites (e.g., quotes vs. movies). Using a relational DB would require rigid schemas and migrations.

## Decision
Use MongoDB as primary storage backend.

## Alternatives
- SQLite: simple, but inflexible for schema changes.
- Postgres: robust, but overkill for prototype.

## Consequences
- Must ensure MongoDB is properly containerized and easy to run.
- Adds minor complexity in deployment, but huge flexibility.
