import pytest
from loguru import logger


@pytest.fixture(autouse=True)
def capture_loguru_logs(caplog):
    import sys

    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
