import pytest
import tempfile
from region_api import settings
import os


@pytest.fixture
def client():
    db_fd, settings.app.config['DATABASE'] = tempfile.mkstemp()
    settings.app.config['TESTING'] = True

    with settings.app.test_client() as client:
        with settings.app.app_context():
            settings.init_db()
        yield client

    os.close(db_fd)
    os.unlink(settings.app.config['DATABASE'])

def test_dummy(client):
    assert 2 == 1, 'test testing'
