from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_view() -> None:
    # TODO: fake data
    name = "Alex"
    params = {"name": name}
    response = client.get("/", params=params)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.text

    expected_message = f"Hello {name}!"
    assert response_data["message"] == expected_message, response_data
