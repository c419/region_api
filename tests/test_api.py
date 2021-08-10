import pytest
import tempfile
from region_api import create_app, API_BASE, logging
from region_api.models import User, City, Region, create_user, db
import os
from base64 import b64encode

class TestConfig:
    SECRET_KEY = 'e095e4e39ed088cfb71600af70357cf1bc8996a1d4e77735'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

login = 'admin'
pwd = '123'

initial_regions = []
initial_regions.append({'name': 'World'})
initial_regions.append({'name': 'Russia', 'parent_id': 1})
initial_regions.append({'name': 'Moscow region', 'parent_id': 2})

initial_cities = []
initial_cities.append({'name': 'Moscow', 'region_id': 3})
initial_cities.append({'name': 'Krasnodar', 'region_id': 2})
initial_cities.append({'name': 'Paris', 'region_id': 1})

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
@pytest.fixture(scope='module')

def token(client):
    basic_creds = b64encode(f'{login}:{pwd}'.encode('ascii')).decode('ascii')
    client_headers = {'Authorization': f'Basic {basic_creds}'}
    logging.debug(f'Client headers are: {client_headers}')
    response = client.get(API_BASE + '/login', headers=client_headers)
    return response.get_json()['token']

           

def test_login(client, token):
    logging.debug(f'Auth token is {token}')
    assert token, 'Token not received during login'

def test_add_region(client, token):
    client_headers = {'Content-Type': 'application/json',
            'x-access-tokens': token}
    for r in initial_regions:
        response = client.post(API_BASE + '/region', headers=client_headers, json=r)
        logging.debug(f'Response status is {response.status}')
        logging.debug(f'Response JSON is {response.get_json()}')
        assert response.status_code == 200, f'API returned {response.status_code}'
        for k in r:
            assert r[k] == response.get_json()[k], f'{k}:{r[k]} sent, but {response.get_json()[k]} received'
        

def test_add_city(client, token):
    client_headers = {'Content-Type': 'application/json',
            'x-access-tokens': token}
    for c in initial_cities:
        response = client.post(API_BASE + '/city', headers=client_headers, json=c)
        logging.debug(f'Response status is {response.status}')
        logging.debug(f'Response JSON is {response.get_json()}')
        assert response.status_code == 200, f'API returned {response.status_code}'
        for k in c:
            assert c[k] == response.get_json()[k], f'{k}:{c[k]} sent, but {response.get_json()[k]} received'
        

def tests_notready():
    assert False, 'Tests aren\'t  ready (yet)'
