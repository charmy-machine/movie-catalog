import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.text

    expected_message = "Hello, Anonymous!"
    assert response_data["message"] == expected_message, response_data


@pytest.mark.parametrize(
    "name",
    [
        # TODO: fake data
        "John",
        "",
        "John Smith",
        "!@#$%",
    ],
)
def test_root_view_custom_name(name: str, client: TestClient) -> None:
    params = {"name": name}
    response = client.get("/", params=params)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.text

    expected_message = f"Hello, {name}!"
    assert response_data["message"] == expected_message, response_data
