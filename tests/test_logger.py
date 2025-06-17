import logging
from app.logger import get_logger, LOG_FILE

def test_logger_returns_same_instance():
    logger1 = get_logger("test")
    logger2 = get_logger("test")
    assert logger1 is logger2

def test_logger_writes_to_file(tmp_path):
    test_log_file = tmp_path / "test.log"
    test_log_dir = test_log_file.parent
    test_log_dir.mkdir(parents=True, exist_ok=True)

    logger_name = "test_logger_file"
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    file_handler = logging.FileHandler(test_log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.info("This is a test log message")

    for handler in logger.handlers:
        handler.flush()

    with open(test_log_file) as f:
        content = f.read()
        assert "This is a test log message" in content

def test_logger_format_and_levels(caplog):
    logger = get_logger("test_format_levels")
    with caplog.at_level(logging.DEBUG):
        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")

    assert "debug message" in caplog.text
    assert "info message" in caplog.text
    assert "warning message" in caplog.text
