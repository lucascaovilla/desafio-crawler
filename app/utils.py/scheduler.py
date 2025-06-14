from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timezone
from app.runner import run_scraper
from app.logger import get_logger

logger = get_logger(__name__)

def schedule_job(args):
    dt = parse_datetime(args.at)
    now = datetime.now(timezone.utc)

    if dt < now:
        logger.error(f"Cannot schedule job in the past: {dt.isoformat()} < {now.isoformat()}")
        print(f"[Error] Cannot schedule job in the past: {dt.isoformat()} < {now.isoformat()}")
        return

    if args.dry_run:
        logger.info(f"[Dry-run] Would schedule job for site '{args.site}' at '{dt.isoformat()}'")
        print(f"[Dry-run] Would schedule job for site '{args.site}' at '{dt.isoformat()}'")
        return

    job_id = f"{args.site}_{dt.isoformat()}"
    logger.info(f"Scheduling job {job_id} for {dt.isoformat()}")

    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(
        run_scraper,
        trigger=DateTrigger(run_date=dt),
        args=[args],
        id=job_id
    )

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Scheduler shutdown requested")
        scheduler.shutdown()

def parse_datetime(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        logger.exception("Invalid datetime format")
        raise ValueError("Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM")
