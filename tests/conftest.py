import pytest
import requests
from urllib.parse import urlparse, urlencode
from hometap_api.secrets import SecretStore

RESPONSES = {
    "/property/geocode?address=123+Fake+St": {"status_code": 400},
    "/property/geocode?address=483+Bright+St+San+Francisco+CA+94132": {
        "status_code": 200,
        "data": {
            "property/geocode": {
                "api_code": 0,
                "api_code_description": "ok",
                "result": True,
            },
            "address_info": {
                "address_full": "483 Bright St San Francisco CA 94132",
                "slug": "483-Bright-St-San-Francisco-CA-94132",
            },
            "status": {"match": True, "errors": []},
        },
    },
    "/property/details?address=483-Bright-St-San-Francisco-CA-94132": {
        "status_code": 200,
        "data": {
            "property/details": {
                "api_code_description": "ok",
                "api_code": 200,
                "result": {
                    "property": {
                        "air_conditioning": "yes",
                        "sewer": "municipal",
                        "style": "colonial",
                        "pool": True,
                    }
                },
            }
        },
    },
}


class MockResponse:
    def __init__(self, endpoint, params):
        self.path = urlparse(endpoint).path
        self.params = urlencode(params)

    def json(self):
        return RESPONSES[f"{self.path}?{self.params}"]["data"]

    @property
    def status_code(self):
        return RESPONSES[f"{self.path}?{self.params}"]["status_code"]


@pytest.fixture(autouse=True)
def path_home(monkeypatch):
    def mock_get_request(endpoint, params, *args, **kwargs):
        return MockResponse(endpoint=endpoint, params=params)

    monkeypatch.setattr(requests, "get", mock_get_request)

    def mock_get_secret(*args, **kwargs):
        return "test_secret"

    monkeypatch.setattr(SecretStore, "get_secret", mock_get_secret)
