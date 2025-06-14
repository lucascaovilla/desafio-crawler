import logging
from app.logger import get_logger, LOG_FILE

def test_logger_returns_same_instance():
    logger1 = get_logger("test")
    logger2 = get_logger("test")
    assert logger1 is logger2

def test_logger_writes_to_file(tmp_path):
    test_log_file = tmp_path / "test.log"

    from app import logger as logger_module
    logger_module.LOG_FILE = str(test_log_file)
    logger_module._logger_initialized = False

    logger = logger_module.get_logger("test_logger_file")
    logger.info("This is a test log message")

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
