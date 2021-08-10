#!/bin/sh
export FLASK_ENV='development'
export FLASK_APP='region_api'
pip install -e .
flask run
