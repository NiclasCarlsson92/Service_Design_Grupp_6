"""
Unit tests for first end-point
"""

import json
import pytest
from app import create_app

# API URL
url = "http://127.0.0.1:5000"

# API TOKEN ID
token_id = "1599bbd0c6e711ec9edea18321551f5a"


@pytest.fixture
def client():
    """
    Test fixture for api client
    :return: yields a test client
    """
    app = create_app()

    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as api_client:
            yield api_client


def test_user_get(client):
    """
    Test the api HTTP status code
    :param token_id: Token id from the fixture
    :return: None
    """
    # Make an API request
    response = client.get(f'/api/v1.0/user/{token_id}')
    # Validating response code
    assert response.status_code == 200


def test_user_get_fail(client):
    """
    Test the api HTTP status code
    :param token_id: Token id from the fixture
    :return: None
    """
    # Make an API request
    response = client.get(f'/api/v1.0/user/zdbdfbkjbvb')
    # Validating response code
    assert response.status_code == 401


def test_user_put(client):
    """
    Test the data from a call to the first end-point
    :param token_id: Token id from the fixture
    :return: None
    """
    # Create an input with JSON format
    request_text = {
        "email": "estani@gmail.com",
        "new password": "casablanca"
    }
    request_json = json.dumps(request_text)
    # Make an API request
    response = client.put(f'/api/v1.0/user/{token_id}', request_json)
    # Validate response code
    assert response.status_code == 200
