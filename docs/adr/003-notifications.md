# ADR 003: Use Telegram and Email for Notifications

## Context
Users should be notified on run success/failure. Email is universal; Telegram is easy to setup for devs.

## Decision
Use Telegram or email (via SMTP or service like Mailgun).

## Alternatives
- SMS: might get expensive
- Slack: great, but not always personal

## Consequences
- Requires `.env` setup for API keys and tokens
- Adds optionality via CLI flags
