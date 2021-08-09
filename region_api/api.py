from flask import Flask, request, abort, jsonify, make_response
from models import db, City, Region, User, sql_exceptions
from settings import app, API_BASE, logging
import itertools
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            logging.debug(token)
        if not token:
            abort(401)
        try:
            data = jwt.decode(token, app.secret_key, algorithms="HS256")
            logging.debug(data)
            current_user = User.query.filter_by(id=data['id']).first()
            logging.debug(f'Token timestamp {data["exp"]}')
            logging.debug(f'Current timestamp is {datetime.datetime.now().timestamp()}')
            if not current_user:
                logging.debug("User not found")
                abort(401)
        except Exception as e:
            logging.debug(e)
            abort(401)
        return f(*args, **kwargs)
    return decorator

@app.route(API_BASE + '/login', methods=['GET', 'POST'])  
def login_user():
    auth = request.authorization   
    if not auth or not auth.username or not auth.password:  
        abort(401)
    user = User.query.filter_by(login=auth.username).first()   
    if check_password_hash(user.password, auth.password):  
        expiration = datetime.datetime.now() + datetime.timedelta(minutes=3)
        logging.debug(f'token expiration timestamp is {expiration.timestamp()}')
        token = jwt.encode({'id': user.id, 'exp' : expiration.timestamp()}, app.config['SECRET_KEY'], algorithm="HS256")  
        return jsonify({'token' : token}) 
    else:
        abort(401)

@app.route(API_BASE + '/city/<int:city_id>', methods=['GET'])
@token_required
def get_city(city_id):
    city = City.query.filter_by(id=city_id).first()
    if city:
        return jsonify(city._api_repr_())
    else:
        abort(404)

@app.route(API_BASE + '/cities', methods=['GET'])
@token_required
def get_cities():
    if not request.json:
        cities = City.query.all()
        return jsonify([c._api_repr_() for c in cities])

    region_id = request.json.get('region_id')
    logging.debug(f'region_id: {region_id}')
    cities = []
    if region_id:
        region = Region.query.filter_by(id=region_id).first()
        if not region:
            abort(404)
        logging.debug(region)
        subregions = region.get_subregions() + [region]
        subregion_cities = [City.query.filter_by(region_id=r.id).all() for r in subregions]
        cities = itertools.chain().from_iterable(subregion_cities)
    else: 
        cities = City.query.all()
    return jsonify([c._api_repr_() for c in cities])

@app.route(API_BASE + '/city', methods=['PUT', 'POST'])
@token_required
def create_city():
    name = request.json.get('name')
    region_id = request.json.get('region_id')
    if not (name and region):
        abort(409)
    try:
        new_city = City(name=name, region_id=region_id)
        db.session.add(new_city)
        db.session.commit()
    except sql_exceptions.IntegrityError:
        abort(409)
    except sql_exceptions.SQLAlchemyError:
        abort(500)
    return jsonify(new_city._api_repr_())

@app.route(API_BASE + '/city/<int:city_id>', methods=['PATCH'])
@token_required
def modify_city(city_id):
    name = request.json.get('name')
    region_id = request.json.get('region_id')
    if not name:
        abort(409)

    city_exist = City.query.filter_by(id=city_id).first()
    if not city_exist:
        abort(404)

    try:
        city_exist.name = name
        city_exist.region_id = region_id
        db.session.commit()
    except sql_exceptions.IntegrityError:
        abort(409)
    except sql_exceptions.SQLAlchemyError:
        abort(500)
    return jsonify(city_exist._api_repr_())


@app.route(API_BASE + '/region/<int:region_id>', methods=['GET'])
@token_required
def get_region(region_id):
    region = Region.query.filter_by(id=region_id).first()
    if region:
        return jsonify(region._api_repr_())
    else:
        abort(404)

@app.route(API_BASE + '/regions', methods=['GET'])
@token_required
def get_regions():
    regions = Region.query.all()
    return jsonify([r._api_repr_() for r in regions])

@app.route(API_BASE + '/region', methods=['PUT', 'POST'])
@token_required
def create_region():
    name = request.json.get('name')
    parent_id = request.json.get('parent_id')
    if not name:
        abort(409)

    try:
        new_region = Region(name=name, parent_id=parent_id)
        db.session.add(new_region)
        db.session.commit()
    except sql_exceptions.IntegrityError:
        abort(409)
    except sql_exceptions.SQLAlchemyError:
        abort(500)
    return jsonify(new_region._api_repr_())

@app.route(API_BASE + '/region/<int:region_id>', methods=['PATCH'])
@token_required
def modify_region(region_id):
    name = request.json.get('name')
    parent_id = request.json.get('parent_id')
    if not name:
        abort(409)

    region_exist = Region.query.filter_by(id=region_id).first()
    if not region_exist:
        abort(404)

    try:
        region_exist.name = name
        region_exist.parent_id = parent_id
        db.session.commit()
    except sql_exceptions.IntegrityError:
        abort(409)
    except sql_exceptions.SQLAlchemyError:
        abort(500)
    return jsonify(region_exist._api_repr_())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
@app.errorhandler(409)
def data_error(error):
    return make_response(jsonify({'error': 'Data integrity error'}), 409)
@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'error': 'Internal server error'}), 500)
@app.errorhandler(401)
def server_error(error):
    return make_response(jsonify({'error': 'Unauthorized'}), 401)



if __name__ == '__main__':
	app.run(debug=True)
