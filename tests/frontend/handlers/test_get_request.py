import pytest
from requests.models import HTTPError
from ui.handlers.get_request import get_request


def test_get_request_success(mock_request_get):
    result = get_request("/test-endpoint")
    assert result == {"key": "value"}


def test_get_request_failure_raises_http_error(mock_request_get):
    with pytest.raises(HTTPError):
        get_request("/bad-endpoint")
