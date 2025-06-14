import os
import json
import tempfile
from app.storage import file, db

sample_data = [{"author": "Ada Lovelace", "text": "Imagination is the key."}]

def test_save_and_read_json():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
        file.save_as_json(sample_data, tf.name)

        with open(tf.name) as f:
            loaded = json.load(f)

        assert loaded == sample_data
        os.remove(tf.name)

def test_store_and_fetch_mongo(monkeypatch):
    mock_data_store = []

    class MockCollection:
        def insert_many(self, docs):
            mock_data_store.extend(docs)

        def find(self, *args, **kwargs):
            return mock_data_store

    class MockDB:
        def __getitem__(self, name):
            return MockCollection()

    class MockClient:
        def __getitem__(self, name):
            return MockDB()

    monkeypatch.setattr("app.storage.db.MongoClient", lambda uri: MockClient())

    test_data = [{"title": "Fake Movie", "year": "2025", "rating": "10.0"}]

    db.store_data("imdb", test_data)
    results = db.fetch_all("imdb")

    assert isinstance(results, list)
    assert results[0]["title"] == "Fake Movie"

def test_store_data_empty(monkeypatch):
    assert db.store_data("quotes", []) is None 
