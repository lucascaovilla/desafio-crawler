def test_take_screenshot_quotes(monkeypatch):
    class MockDriver:
        def get(self, url): pass
        def save_screenshot(self, filename): self.filename = filename
        def quit(self): pass

    class MockOptions:
        def add_argument(self, arg): pass

    monkeypatch.setattr("app.utils.screenshot.webdriver.Chrome", lambda options: MockDriver())
    monkeypatch.setattr("app.utils.screenshot.Options", lambda: MockOptions())

    from app.utils.screenshot import take_screenshot
    take_screenshot("quotes")

def test_take_screenshot_imdb(monkeypatch):
    class MockDriver:
        def get(self, url):
            assert "imdb.com" in url
        def save_screenshot(self, filename): pass
        def quit(self): pass

    class MockOptions:
        def add_argument(self, arg): pass

    monkeypatch.setattr("app.utils.screenshot.webdriver.Chrome", lambda options: MockDriver())
    monkeypatch.setattr("app.utils.screenshot.Options", lambda: MockOptions())

    from app.utils.screenshot import take_screenshot
    take_screenshot("imdb")
