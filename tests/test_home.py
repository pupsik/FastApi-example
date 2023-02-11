from fastapi.testclient import TestClient

from hometap_api.app import app
from hometap_api.secrets import SecretStore
from hometap_api.v1.clients.house_canary import HouseCanaryAPIClient

from .conftest import mock_get_request, mock_get_secret

client = TestClient(app)


def test_read_home_200():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_has_septic_system_200(monkeypatch):
    monkeypatch.setattr(SecretStore, "get_secret", mock_get_secret)
    monkeypatch.setattr(HouseCanaryAPIClient, "get", mock_get_request)
    response = client.get("/api/has_septic_system?address=123")
    assert response.status_code == 200
    assert response.json() == {"has_septic_system": False}
