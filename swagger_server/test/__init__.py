import logging

import connexion
from flask_testing import TestCase
import os

from swagger_server.encoder import JSONEncoder

from swagger_server.model import db, PnaSpecies, PnaSpecimen, PnaUser, PnaRole

class BaseTestCase(TestCase):

    api_key = "AnyThingBecAuseThIsIsATEST123456"
    api_key2 = "AnyThingBecAuseThIsIsATEST567890"

    def setUp(self):
        db.create_all()
        self.user1 = PnaUser(user_id=100,
                name="test_user",
                api_key=self.api_key)
        db.session.add(self.user1)
        self.user2 = PnaUser(user_id=200,
                name="test_user_admin",
                api_key=self.api_key2)
        db.session.add(self.user2)
        self.role = PnaRole(role="admin")
        self.role.user = self.user2
        db.session.add(self.role)
        self.species1 = PnaSpecies(common_name="lugworm",
                family="Arenicolidae",
                genus="Arenicola",
                tax_order="None",
                phylum="Annelida",
                prefix="wuAreMari",
                name="Arenicola marina",
                tax_class="Polychaeta",
                taxonomy_id=6344)
        db.session.add(self.species1)
        self.species2 = PnaSpecies(common_name="human",
                family="Hominidae",
                genus="Homo",
                tax_order="Primates",
                phylum="Chordata",
                prefix="mHomSap",
                name="Homo sapiens",
                tax_class="Mammalia",
                taxonomy_id=9606)
        db.session.add(self.species2)
        self.specimen1 = PnaSpecimen(specimen_id="SAN0000100", number=1, public_name="wuAreMari1")
        self.specimen1.species = self.species1
        self.specimen1.user = self.user1
        db.session.add(self.specimen1)
        db.session.commit()

    def tearDown(self):
        db.session.query(PnaSpecimen).delete()
        db.session.query(PnaSpecies).delete()
        db.session.query(PnaRole).delete()
        db.session.query(PnaUser).delete()
        db.session.commit()

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml', pythonic_params=True)
        app.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
        app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app.app)
        return app.app
