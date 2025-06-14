import subprocess
import sys
import json

def test_cli_help():
    result = subprocess.run([sys.executable, "main.py", "--help"], capture_output=True, text=True)
    assert "usage:" in result.stdout
    assert "scrape" in result.stdout
    assert result.returncode == 0

def test_cli_scrape_quotes_json(tmp_path):
    output_path = tmp_path / "quotes.json"
    result = subprocess.run([
        sys.executable, "main.py", "scrape", "quotes", "--format", "json", "--output", str(output_path), "--no-screenshot"
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert output_path.exists()
    with open(output_path) as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert all("text" in item and "author" in item for item in data)

def test_cli_schedule_echo():
    result = subprocess.run(
        [sys.executable, "main.py", "schedule", "quotes", "--at", "2030-01-01T00:00:00", "--dry-run"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[Dry-run]" in result.stdout
    assert "quotes" in result.stdout

def test_cli_show_quotes():
    result = subprocess.run(
        [sys.executable, "main.py", "show", "quotes"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    stdout = result.stdout.lower()
    assert "no data" in stdout or "text" in stdout

def test_cli_unknown_command(capsys):
    from app.cli import dispatch
    class Args:
        command = "unknown"
    dispatch(Args())
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out
