"""tests made for our api"""
import pytest
from app import create_app


@pytest.fixture
def client():
    """client yields an api_client from our flask_application"""
    app_testing = create_app()

    app_testing.config['TESTING'] = True

    with app_testing.app_context():
        with app_testing.test_client() as api_client:
            yield api_client


def test_user_api(client):
    """testing the user api"""
    response = client.get('/api/v1.0/user/b1df1fb2cae011eca11ab06ebfd0e3f3')
    print(response.status_code)
    assert response.status_code == 200
