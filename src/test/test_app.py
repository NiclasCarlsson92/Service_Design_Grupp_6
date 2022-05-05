import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()

    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as api_client:
            yield api_client


def test_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200
