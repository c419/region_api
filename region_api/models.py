from flask import current_app 
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from werkzeug.security import generate_password_hash
sql_exceptions = sqlalchemy.exc

db = SQLAlchemy()

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True) 
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    region = db.relationship('Region', back_populates='city')
    def __repr__(self):
        return self.name
    def _api_repr_(self):
        return {'id': self.id, 'name': self.name, 'region_id': self.region_id}

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    parent_id = db.Column(db.Integer)
    city = db.relationship('City', back_populates='region')
    def __repr__(self):
        return self.name
    def _api_repr_(self):
        return {'id': self.id, 'name': self.name, 'parent_id': self.parent_id}
    def get_subregions(self):
        return Region.query.filter_by(parent_id=self.id).all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean)


def create_user(login, password):
    new_user = User(login=login, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
