import time
from app.utils.mailjet_email import send_email
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
        print(f"Cannot schedule job in the past: {dt.isoformat()} < {now.isoformat()}")
        return

    if args.dry_run:
        logger.info(f"[Dry-run] Would schedule job for site '{args.site}' at '{dt.isoformat()}'")
        print(f"[Dry-run] Would schedule job for site '{args.site}' at '{dt.isoformat()}'")
        return

    job_id = f"{args.site}_{dt.isoformat()}"
    logger.info(f"Scheduling job {job_id} for {dt.isoformat()}")

    try:
        if hasattr(args, "notify_to"):
            confirm_message = f"A scraper run for site '{args.site}' has been scheduled for {dt.isoformat()}."
            send_email(args.notify_to, "Crawler Job Scheduled", confirm_message)
            logger.info(f"Scheduling confirmation sent to {args.notify_to}")
    except Exception as e:
        logger.exception("Failed to send scheduling confirmation email")

    scheduler = BackgroundScheduler()
    scheduler.start()

    def job_with_notification():
        run_scraper(args)
        message = f"Scraper run for site '{args.site}' completed at {datetime.now(timezone.utc).isoformat()}"
        try:
            if hasattr(args, "notify_to"):
                send_email(args.notify_to, "Notification from Crawler", message)
                logger.info(f"Notification sent to {args.notify_to}")
        except Exception as e:
            logger.exception("Failed to send completion notification")

    scheduler.add_job(
        job_with_notification,
        trigger=DateTrigger(run_date=dt),
        id=job_id
    )

    try:
        while scheduler.get_job(job_id):
            time.sleep(1)
        logger.info("Job completed. Shutting down scheduler.")
        scheduler.shutdown()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down scheduler.")
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
