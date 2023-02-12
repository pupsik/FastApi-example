from fastapi.testclient import TestClient

from hometap_api.app import app

client = TestClient(app)


def test_read_home_200():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_has_septic_system_200():
    response = client.get(
        "/api/has_septic_system?address=483 Bright St San Francisco CA 94132"
    )
    assert response.status_code == 200
    assert response.json() == {"has_septic_system": False}


def test_has_septic_system_422():
    response = client.get("/api/has_septic_system")
    assert response.status_code == 422


def test_has_septic_system_503():
    response = client.get("/api/has_septic_system?address=123+Fake+St")
    assert response.status_code == 503
