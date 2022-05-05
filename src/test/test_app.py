import pytest
from app import create_app


@pytest.fixture
def client():
    app_testing = create_app()

    app_testing.config['TESTING'] = True

    with app_testing.app_context():
        with app_testing.test_client() as api_client:
            yield api_client


def test_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200
