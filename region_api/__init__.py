from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import os

API_VER = 'v1.0'
API_NAME = 'region_api'
API_BASE = f'/{API_NAME}/{API_VER}'
db = SQLAlchemy()
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(funcName)s %(message)s')

def create_app(config=None):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    db_path = filename = os.path.join(app.root_path, 'database')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_path, 'api.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    logging.debug(app.config)
    if config:
        app.config.from_object(config)
	
    from region_api.models import db
    db.init_app(app)

    with app.app_context():
        from . import api
        return app



