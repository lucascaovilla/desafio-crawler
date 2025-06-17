from app.scrapers import quotes_scraper, imdb_scraper


def test_scrape_returns_list_of_quotes(monkeypatch):
    sample_html = """
    <div class="quote">
        <span class="text">“Be yourself; everyone else is already taken.”</span>
        <small class="author">Oscar Wilde</small>
    </div>
    """

    class MockResponse:
        def __init__(self):
            self.text = sample_html

        def raise_for_status(self): pass

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    result = quotes_scraper.scrape()
    assert isinstance(result, list)
    assert result[0]["author"] == "Oscar Wilde"
    assert "Be yourself" in result[0]["text"]


def test_scrape_returns_list_of_imdb_movies(monkeypatch):
    class MockElement:
        def __init__(self, text=""):
            self._text = text

        def find_element(self, by, value):
            if "imdbRating" in value:
                return MockElement("9.3")
            elif "span" in value or "year" in value:
                return MockElement("(1994)")
            elif "a" in value:
                return MockElement("The Shawshank Redemption")
            return MockElement("")

        @property
        def text(self):
            return self._text

    result = imdb_scraper.scrape()

    assert isinstance(result, list)
    assert len(result) == 25
    assert result[0]["title"] == "1. The Shawshank Redemption"
    assert result[0]["year"] == "1994"
    assert result[0]["rating"] == "9.3"
