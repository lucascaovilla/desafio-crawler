def test_save_as_csv(tmp_path):
    filename = tmp_path / "test.csv"
    data = [{"name": "Alice", "score": 10}]
    from app.storage.file import save_as_csv

    save_as_csv(data, filename)
    assert filename.exists()
    content = filename.read_text()
    assert "Alice" in content

def test_save_as_csv_no_data(capfd):
    from app.storage.file import save_as_csv
    save_as_csv([], "dummy.csv")
    out, _ = capfd.readouterr()
    assert "No data to save." in out
