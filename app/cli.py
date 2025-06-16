import argparse
from app.utils.scheduler import schedule_job
from app.runner import run_scraper, show_data
from app.logger import get_logger

logger = get_logger(__name__)

def dispatch(args):
    logger.debug(f"Dispatching command: {args.command}")
    if args.command == "scrape":
        run_scraper(args)
    elif args.command == "schedule":
        schedule_job(args)
    elif args.command == "show":
        show_data(args)
    else:
        logger.error(f"Unknown command received: {args.command}")
        print("Unknown command")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    scrape_parser = subparsers.add_parser("scrape")
    scrape_parser.add_argument("site", choices=["quotes", "imdb"])
    scrape_parser.add_argument("--format", choices=["json", "csv"], default="json")
    scrape_parser.add_argument("--output", help="Path to output file")
    scrape_parser.add_argument("--no-screenshot", action="store_true", help="Skip screenshots")

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("site", choices=["quotes", "imdb"])
    show_parser.add_argument("--all", action="store_true", help="Show all data instead of just the first few rows")

    schedule_parser = subparsers.add_parser("schedule")
    schedule_parser.add_argument("site", choices=["quotes", "imdb"])
    schedule_parser.add_argument("--at", help="Time to run job (ISO format)", required=True)
    schedule_parser.add_argument("--dry-run", action="store_true", help="Print schedule plan without executing")
    schedule_parser.add_argument("--notify-to", help="Recipient for notifications")
    schedule_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    schedule_parser.add_argument("--output", help="Path to output file")

    args = parser.parse_args()
    dispatch(args)
