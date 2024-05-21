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


def test_get_data_without_token(client):
    """
    Test case to verify the behavior of the API when accessed without a token.

    This test case sends a GET request to the '/api/data/0968599020001' endpoint 
    without providing an authentication token. It then asserts that the response 
    status code is 401 (Unauthorized) and that the response JSON contains the 
    expected error message.

    Parameters:
        client (FlaskClient): The Flask test client object.

    Returns:
        None
    """
    response = client.get('/api/data/0968599020001')
    assert response.status_code == 401
    assert response.get_json() == {
        'message': 'Authentication token is missing. Please provide a valid token to access this resource.'}

def test_get_data_with_valid_token_and_id(client, create_token):
    """
    Test case to verify the functionality of the `get_data_with_valid_token` function.

    This test case checks if the `get_data_with_valid_token` function returns a successful response (status code 200) when a valid token is provided in the request headers
    and get info or returns a failed response (status code 404) when a valid token is provided in the request headers but not get info for id

    Parameters:
    - client: The Flask test client object used to send HTTP requests.
    - create_token: A fixture that creates a token for testing the API authentication.

    Returns:
        None
    """
    headers = {
        'Authorization': f'Bearer {create_token}'
    }
    response = client.get('/api/data/0968599020001', headers=headers)
    if response.get_json()['msg'] == 'ID not found':
        assert response.status_code == 404
    else:
        assert response.status_code == 200


def test_get_data_with_invalid_id(client, create_token):
    """
    Test case to verify the functionality of the `get_data_with_invalid_id` function.

    This test case checks if the `get_data_with_invalid_id` function returns a 404 status code and the correct error message when an invalid ID.

    Parameters:
    - client: The Flask test client object used to send HTTP requests.
    - create_token: A fixture that creates a token for testing the API authentication.

    Returns:
        None
    """
    headers = {
        'Authorization': f'Bearer {create_token}'
    }
    response = client.get('/api/data/1', headers=headers)

    assert response.status_code == 404
    assert response.get_json()['msg'] == 'ID not found'
