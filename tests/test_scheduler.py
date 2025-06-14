def test_parse_datetime_valid():
    from app.utils.scheduler import parse_datetime
    assert parse_datetime("2025-01-01T12:00").year == 2025

def test_parse_datetime_invalid():
    from app.utils.scheduler import parse_datetime
    import pytest
    with pytest.raises(ValueError):
        parse_datetime("not-a-date")

def test_schedule_real_job(monkeypatch):
    from app.utils import scheduler

    class DummyScheduler:
        def start(self): self.started = True
        def add_job(self, *args, **kwargs): self.job_added = True
        def shutdown(self): self.shutdown_called = True

    monkeypatch.setattr("app.utils.scheduler.BackgroundScheduler", lambda: DummyScheduler())
    monkeypatch.setattr("app.utils.scheduler.run_scraper", lambda x: None)
    monkeypatch.setattr("builtins.print", lambda x: None)

    class Args:
        site = "quotes"
        at = "2030-01-01T00:00:00"
        dry_run = False

    import signal

    def raise_keyboard_interrupt(signum, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGALRM, raise_keyboard_interrupt)
    signal.alarm(1)

    try:
        scheduler.schedule_job(Args())
    except KeyboardInterrupt:
        pass
    finally:
        signal.alarm(0)
