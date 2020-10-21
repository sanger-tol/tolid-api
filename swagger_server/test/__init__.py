import logging

import connexion
from flask_testing import TestCase
import os
import json

from swagger_server.encoder import JSONEncoder
from swagger_server.controllers.curators_controller import db_file_name, verify_database


class BaseTestCase(TestCase):

    with open(os.path.join('instance', 'config.json')) as config_file:
        config = json.load(config_file)
        tokens = config['api-keys']  # Read API-Tokens from the global config file
        api_keys = list(tokens.keys())
        api_key = api_keys[0]

    def setUp(self):
        # For now, a new version of the database for each test
        os.remove(db_file_name)
        verify_database()

    def tearDown(self):
        #TODO
        pass

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml', pythonic_params=True)
        return app.app
