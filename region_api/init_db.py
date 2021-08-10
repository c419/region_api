from region_api.models import create_schema, User, db, create_user
from region_api import create_app

app = create_app()
with app.app_context():
    create_schema()
    create_user('admin', '123')
