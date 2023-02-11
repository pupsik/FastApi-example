import requests
from requests.auth import HTTPBasicAuth

from hometap_api.v1.exceptions import HouseCanaryApiException
from hometap_api.v1.settings import SETTINGS

SECRETS_DIR = SETTINGS.secrets_dir


class HouseCanaryAPIClient:
    url: str = SETTINGS.house_canary_url
    headers: dict[str, str] = {"Content-Type": "application/json"}
    auth: tuple | HTTPBasicAuth

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(self, endpoint, params=None):
        response = requests.get(
            f"{self.url}/{endpoint}",
            params=params,
            headers=self.headers,
            auth=self.auth,
            timeout=5,
        )
        # TODO: Add logging for all third-party api response codes
        if not response.status_code == 200:
            # This error will be intercepted by the middleware
            # and will always return 503 error to the web client; 
            raise HouseCanaryApiException
        return response
