RESPONSES = {
    "property/geocode": {
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
    "property/details": {
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
}


class MockResponse:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def json(self):
        return RESPONSES[self.endpoint]


def mock_get_request(cls, endpoint, *args, **kwargs):
    return MockResponse(endpoint=endpoint)


def mock_get_secret(*args, **kwargs):
    return "test_secret"
