import os
from functools import wraps

import itsdangerous
from flask import request, jsonify, make_response

from modules import logger
from modules.app import app
from modules.database import find_user_by_username
from modules.database.crud.crud_user import add_user, find_user_by_email
from modules.database.models.ot_user_t import User

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/register', methods=['POST'])
def register_new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if username is None or password is None or email is None:
        status_code = 400
        data = {'status': 'failed', 'message': 'Missing arguments'}
        return make_response(jsonify(data), status_code)
    if find_user_by_username(username) is not None:
        status_code = 409
        data = {'status': 'failed', 'message': 'Username {username} already exist'}
        return make_response(jsonify(data), status_code)
    if find_user_by_email(email) is not None:
        status_code = 409
        data = {'status': 'failed', 'message': 'Email {email} already exist'}
        return make_response(jsonify(data), status_code)
    user = User(username, password, email)
    status_code, resource_id = add_user(user)
    data = {'status': 'success', 'message': 'Created resource_id {resource_id}'}
    return make_response(jsonify(data), status_code)


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        status_code = 400
        data = {'status': 'failed', 'message': 'Missing arguments'}
        return make_response(jsonify(data), status_code)
    user = find_user_by_email(email)
    if user is None:
        status_code = 404
        data = {'status': 'failed', 'message': 'Account do not exist'}
        return make_response(jsonify(data), status_code)
    if not user.verify_password(password):
        status_code = 401
        data = {'status': 'failed', 'message': 'Wrong password'}
        return make_response(jsonify(data), status_code)
    status_code = 200
    token = encode_auth_token(user.id)
    data = {'status': 'success', 'message': 'Login successful', 'token': token.decode('ascii')}
    return make_response(jsonify(data), status_code)


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        AUTHORIZATION_KEY = 'Authorization'
        if not request.headers.has_key(AUTHORIZATION_KEY):
            data = {'status': 'failed', 'message': 'Add authorization key to header'}
            return make_response(jsonify(data), 401)

        auth_token = request.headers.get(AUTHORIZATION_KEY)
        resp = decode_auth_token(auth_token)

        if not isinstance(resp, int):
            data = {'status': 'failed', 'message': resp}
            return make_response(jsonify(data), 401)
        return f(resp, **kwargs)
    return decorated_function


def encode_auth_token(user_id, expiration=600):
    s = itsdangerous.TimedJSONWebSignatureSerializer(app.config['JWT_SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user_id})


def decode_auth_token(token):
    s = itsdangerous.TimedJSONWebSignatureSerializer(app.config['JWT_SECRET_KEY'])
    try:
        data = s.loads(token)
        return data['id']
    except itsdangerous.SignatureExpired:
        return 'Signature expired. Please log in again.'
    except itsdangerous.BadSignature:
        return 'Invalid token. Please log in again.'
