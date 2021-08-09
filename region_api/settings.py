from flask import Flask
import logging

API_VER = 'v1.0'
API_NAME = 'region_api'
API_BASE = f'/{API_NAME}/{API_VER}'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
logging.basicConfig(filename='api.log', level=logging.DEBUG, format='%(asctime)s %(funcName)s %(message)s')
