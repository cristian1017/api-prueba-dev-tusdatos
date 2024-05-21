import pytest
from app import create_app


@pytest.fixture
def client():
    """
    Fixture that creates a Flask test client for testing the application.

    Returns:
        FlaskClient: A Flask test client for testing the application.

    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_auth_succes(client):
    """
    Test the success scenario of the authentication API.

    This function sends a POST request to the "/api/login/" endpoint with the 
    provided username and password in the request payload. It then asserts 
    that the response status code is 200 and the response JSON contains the 
    message "Login Success".

    Parameters:
        client (FlaskClient): The Flask test client object.

    Returns:
        None
    """
    response = client.post(
        "/api/login", json={"username": "tusdatos", "password": "123456"})
    assert response.status_code == 200
    assert response.get_json()['msg'] == "Login Success"


def test_auth_credentials_incorrect(client):
    """
    Test the authentication API with incorrect credentials.

    This function sends a POST request to the "/api/login/" endpoint with the provided 
    username and password in the request payload. It then asserts that the response status 
    code is 401 and the response JSON contains the message "Invalid username or password".

    Parameters:
        client (FlaskClient): The Flask test client object.

    Returns:
        None
    """
    response = client.post(
        "/api/login", json={"username": "cristian", "password": "19832467"})
    assert response.status_code == 401
    assert response.get_json()['msg'] == "Invalid username or password"


def test_auth_without_payload(client):
    """
    Test the authentication API without a payload.

    This function sends a POST request to the "/api/login/" endpoint without a payload.
    It then asserts that the response status code is 400 and the response JSON contains
    the message "Invalid JSON payload".

    Parameters:
        client (FlaskClient): The Flask test client object.

    Returns:
        None
    """
    response = client.post(
        "/api/login", headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert response.get_json()['msg'] == "Invalid JSON payload"
