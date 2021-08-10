import pytest
import tempfile
from region_api import create_app, API_BASE
from region_api.models import User, City, Region, create_user, db
import os
from base64 import b64encode

class TestConfig:
    SECRET_KEY = 'e095e4e39ed088cfb71600af70357cf1bc8996a1d4e77735'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

login = 'admin'
pwd = '123'
basic_creds = b64encode(f'{login}:{pwd}'.encode('utf-8'))

def init_db():
    db.create_all()
    create_user(login, pwd)


@pytest.fixture(scope='module')
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            init_db()
            yield client

def test_dummy(client):
    assert 1 == 1, 'test testing'

def test_login(client):
    response = client.get(API_BASE + '/login', headers={'Authorization': f'Basic {basic_creds}'})
    print(response)
    assert False
