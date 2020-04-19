import os
from flask import Flask, request, jsonify
from api.config import app_config
from parser.parser import parse
import requests
from multiprocessing import Process

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
    response = {
            'error': 'None',
            'data': data
        }
    header = {'Content-Type': 'application/json'}
    r = requests.post(callback_url, headers=header, data=response)
    print(r.status)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.app_context().push()

    @app.route('/', methods=['POST'])
    def get_document_link():
        p = ParseProcess(run_parse)
        global document_url, callback_url
        document_url = request.json['document_url']
        callback_url = request.json['callback_url']
        p.start()
        return jsonify({'error': None, 'status': 'Ok'}), 200



    return app
