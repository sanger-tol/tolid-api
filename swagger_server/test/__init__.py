import logging

import connexion
from flask_testing import TestCase
import os
import json

from swagger_server.encoder import JSONEncoder
from swagger_server.controllers.curators_controller import db_file_name, verify_database

from swagger_server.model import db, PnaSpecies, PnaSpecimen

class BaseTestCase(TestCase):

    with open(os.path.join('instance', 'config.json')) as config_file:
        config = json.load(config_file)
        tokens = config['api-keys']  # Read API-Tokens from the global config file
        api_keys = list(tokens.keys())
        api_key = api_keys[0]

    def setUp(self):
        db.create_all()
        species1 = PnaSpecies(common_name="lugworm",
                family="Arenicolidae",
                genus="Arenicola",
                tax_order="None",
                phylum="Annelida",
                prefix="wuAreMari",
                name="Arenicola marina",
                tax_class="Polychaeta",
                taxonomy_id=6344)
        db.session.add(species1)
        species2 = PnaSpecies(common_name="human",
                family="Hominidae",
                genus="Homo",
                tax_order="Primates",
                phylum="Chordata",
                prefix="mHomSap",
                name="Homo sapiens",
                tax_class="Mammalia",
                taxonomy_id=9606)
        db.session.add(species2)
        specimen1 = PnaSpecimen(specimen_id="SAN0000100", number=1)
        specimen1.species = species1
        db.session.add(specimen1)
        db.session.commit()
        
        # For now, a new version of the database for each test
        os.remove(db_file_name)
        verify_database()

    def tearDown(self):
        db.session.query(PnaSpecimen).delete()
        db.session.query(PnaSpecies).delete()
        db.session.commit()

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml', pythonic_params=True)
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app.app)
        return app.app
