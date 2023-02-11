import requests
from requests.auth import HTTPBasicAuth

from hometap_api.v1.settings import SETTINGS

SECRETS_DIR = SETTINGS.secrets_dir


class HouseCanaryAPIClient:
    root: str = "https://virtserver.swaggerhub.com/RITALINETS/HouseCanaryMock"
    version: str = "1.0.0"
    headers: dict[str, str] = {"Content-Type": "application/json"}
    auth: tuple | HTTPBasicAuth

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def url(self):
        return f"{self.root}/{self.version}"

    def get(self, endpoint, params=None):
        print(
            f"{self.url}/{endpoint}",
        )
        return requests.get(
            f"{self.url}/{endpoint}",
            params=params,
            headers=self.headers,
            auth=self.auth,
        )
