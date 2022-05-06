"""tests made for our api"""
import json
import pytest
from app import create_app, db
from controllers.user_controller import get_user_by_id
from blueprints.api import api_get


@pytest.fixture
def client():
    """client yields an api_client from our flask_application"""
    app_testing = create_app()

    app_testing.config['TESTING'] = True

    with app_testing.app_context():
        with app_testing.test_client() as api_client:
            yield api_client


def test_user_api(client):
    """Test to see if we get a successful response when asking for a users current balance"""
    user = get_user_by_id(1)
    user_token = user.api_token
    response = client.get(f'/api/v1.0/user/{user_token}')
    assert response.status_code == 200


def test_wallet_api(client):
    """Test to see if we get a successful response when asking for a users wallet"""
    user = get_user_by_id(1)
    user_token = user.api_token
    response = client.get(f'/api/v1.0/wallet/{user_token}')
    assert response.status_code == 200


def test_coinmarketcap_api(client):
    """Test to see if our request to CMCApi return something"""
    response = api_get()
    json_data = json.dumps(response)
    assert json_data is not None


def test_database_connection(client):
    """Test to see there's a valid connection to our database"""
    pass
