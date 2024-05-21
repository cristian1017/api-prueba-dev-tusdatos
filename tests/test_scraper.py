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


@pytest.fixture
def create_token(client):
    """
    Fixture that creates a token for testing the API authentication.
    This fixture sends a POST request to the "/api/login/" endpoint with the provided username and password in the request payload.
    It then asserts that the response status code is 200 and returns the token from the response JSON.
    Parameters:
        client (FlaskClient): The Flask test client object.
    Returns:
        str: The token obtained from the response JSON.
    """
    response = client.post(
        "/api/login", json={"username": "tusdatos", "password": "123456"})
    assert response.status_code == 200
    return response.get_json()['token']


def test_scraper_with_valid_token(client, create_token):
    """
    Test case to verify the functionality of the `scraper` endpoint with a valid token.

    This test case checks if the `scraper` endpoint returns a successful response (status code 200) when a valid token is provided in the request headers. It also checks if the response JSON contains the message 'The scraping process has been completed'.

    Parameters:
    - client: The Flask test client object used to send HTTP requests.
    - create_token: A fixture that creates a token for testing the API authentication.

    Returns:
        None
    """
    headers = {
        'Authorization': f'Bearer {create_token}'
    }
    response = client.get('/api/scraper', headers=headers)
    assert response.status_code == 200
    assert response.get_json(
    )['msg'] == 'The scraping process has been completed'


def test_scraper_without_token(client):
    """
    Test case to verify the functionality of the `scraper` endpoint without a token.

    This test case checks if the `scraper` endpoint returns a 401 status code and the correct error message when no token is provided in the request headers.

    Parameters:
    - client: The Flask test client object used to send HTTP requests.

    Returns:
        None
    """
    response = client.get('/api/scraper')
    assert response.status_code == 401
    assert response.get_json() == {
        'message': 'Authentication token is missing. Please provide a valid token to access this resource.'
    }
