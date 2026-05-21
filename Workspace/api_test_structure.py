import pytest
import requests

BASE_URL = "https://httpbin.org"

@pytest.mark.parametrize("method,endpoint,data", [
    ("get", "/get", None),
    ("post", "/post", {"key": "value"}),
    ("put", "/put", {"key": "value"}),
    ("patch", "/patch", {"key": "value"}),
    ("delete", "/delete", None),
])
def test_api_methods(method, endpoint, data):
    url = BASE_URL + endpoint
    func = getattr(requests, method)
    if data:
        response = func(url, json=data)
    else:
        response = func(url)
    assert response.status_code == 200
    assert response.json() is not None
