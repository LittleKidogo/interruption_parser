import os
from flask import Flask, request, jsonify
import requests
from multiprocessing import Process
from api.config import app_config
from parser.parser import parse
from api.util import validate_url

document_url = None
callback_url = None

class ParseProcess(Process):

    def __init__(self, function):
        Process.__init__(self)
        self.daemon = True
        self.target = function

    def run(self):
        self.target()


def run_parse():
    global document_url, callback_url
    data = parse(document_url)
    headers = {'Content-Type': 'application/json'}
    if data is None:
        requests.post(callback_url, headers=headers, data={'error' : 'couldn\'t parse the requested document', data: None})
        return
    response = {
            'error': 'None',
            'data': data
        }
    requests.post(callback_url, headers=headers, data=response)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.app_context().push()

    @app.route('/', methods=['POST'])
    def get_document_link():
        global document_url, callback_url
        p = ParseProcess(run_parse)

        document_url = request.json['document_url']
        callback_url = request.json['callback_url']

        if type(document_url) is not str or type(callback_url) is not str:
            return jsonify({'error': 'invalid types. input must be string', 'status': 'fail'}), 409

        elif not validate_url(document_url) or not validate_url(callback_url):
            return jsonify({'error': 'invalid urls', 'status': 'fail'}), 409

        p.start()
        return jsonify({'error': None, 'status': 'Ok'}), 200



    return app
