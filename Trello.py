import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})

from modules import logger
from modules.app import app

# Create a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    LOG.info('root')
    return make_response(jsonify({'hello': 'Hello Flask'}), 200)

if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('ENV'))
    os.environ['SECRET'] = 'c3c4HTQX6ETCdGrJ8dXS'
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run()

