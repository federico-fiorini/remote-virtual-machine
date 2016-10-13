from flask import Flask, make_response, jsonify
from flask_httpauth import HTTPTokenAuth
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config')

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    if token == app.config['AUTHORIZATION_KEY']:
        return True
    return False


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'status': 'ERROR', 'message': 'Unauthorized access'}), 403)

from app import views