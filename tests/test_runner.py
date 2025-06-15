
import pytest
from app.runner import run_scraper

def test_run_scraper(monkeypatch):
    class Args:
        site = "quotes"
        format = "json"
        output = "test_output.json"
        no_screenshot = False

    mock_data = [{"author": "Grace Hopper", "text": "Debugging is fun."}]

    monkeypatch.setattr("app.runner.quotes_scraper.scrape", lambda: mock_data)
    monkeypatch.setattr("app.runner.file.save_as_json", lambda data, path: None)
    monkeypatch.setattr("app.runner.take_screenshot", lambda site: None)
    monkeypatch.setattr("app.runner.db.store_data", lambda site, data: None)

    run_scraper(Args())

def test_run_scraper_unknown_site_full():
    class Args:
        site = "unknown"
        format = "json"
        output = None
        no_screenshot = True

    with pytest.raises(ValueError, match="Unknown site"):
        run_scraper(Args())


def test_run_scraper_csv(monkeypatch, tmp_path):
    class Args:
        site = "quotes"
        format = "csv"
        output = tmp_path / "out.csv"
        no_screenshot = True

    monkeypatch.setattr("app.scrapers.quotes_scraper.scrape", lambda: [{"text": "hi", "author": "me"}])
    monkeypatch.setattr("app.storage.file.save_as_csv", lambda data, path: open(path, "w").write("dummy csv"))
    monkeypatch.setattr("app.storage.db.store_data", lambda site, data: None)

    run_scraper(Args())
    assert Args.output.exists()

def test_run_scraper_with_screenshot(monkeypatch, tmp_path):
    from app.runner import run_scraper

    class Args:
        site = "imdb"
        format = "json"
        output = tmp_path / "out.json"
        no_screenshot = False

    monkeypatch.setattr("app.scrapers.imdb_scraper.scrape", lambda: [{"title": "Oppenheimer", "rating": "9.0"}])
    monkeypatch.setattr("app.storage.file.save_as_json", lambda data, path: open(path, "w").write("[]"))
    monkeypatch.setattr("app.storage.db.store_data", lambda site, data: None)

    class MockDriver:
        def get(self, url): assert "imdb.com" in url
        def save_screenshot(self, filename): pass
        def quit(self): pass

    class MockOptions:
        def add_argument(self, arg): pass

    monkeypatch.setattr("app.utils.screenshot.webdriver.Chrome", lambda options: MockDriver())
    monkeypatch.setattr("app.utils.screenshot.Options", lambda: MockOptions())

    run_scraper(Args())

    assert Args.output.exists()
