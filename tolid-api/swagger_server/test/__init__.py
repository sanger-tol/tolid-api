import logging

import connexion
from flask_testing import TestCase
import os

from swagger_server.encoder import JSONEncoder

from swagger_server.model import db, TolidSpecies, TolidSpecimen, \
    TolidUser, TolidRole, TolidRequest, TolidState


class BaseTestCase(TestCase):

    api_key = "AnyThingBecAuseThIsIsATEST123456"
    api_key2 = "AnyThingBecAuseThIsIsATEST567890"
    api_key3 = "AnyThingBecAuseThIsIsATEST24680"

    def setUp(self):
        self.maxDiff = None
        db.create_all()
        self.user1 = TolidUser(user_id=100,
                               name="test_user_requester",
                               email="test_user_requester@sanger.ac.uk",
                               organisation="Sanger Institute",
                               api_key="AnyThingBecAuseThIsIsATEST123456")
        db.session.add(self.user1)
        self.user2 = TolidUser(user_id=200,
                               name="test_user_admin",
                               email="test_user_admin@sanger.ac.uk",
                               organisation="Sanger Institute",
                               api_key="AnyThingBecAuseThIsIsATEST567890")
        db.session.add(self.user2)
        self.user3 = TolidUser(user_id=300,
                               name="test_user_creator",
                               email="test_user_creator@sanger.ac.uk",
                               organisation="Sanger Institute",
                               api_key="AnyThingBecAuseThIsIsATEST24680")
        self.user4 = TolidUser(user_id=400,
                               name="test_user_requester2",
                               email="test_user_requester2@sanger.ac.uk",
                               organisation="Sanger Institute",
                               api_key="AnyThingBecAuseThIsIsATEST13579")
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.add(self.user3)
        db.session.add(self.user4)
        self.role = TolidRole(role="admin")
        self.role.user = self.user2
        db.session.add(self.role)
        self.role = TolidRole(role="creator")
        self.role.user = self.user3
        db.session.add(self.role)
        self.species1 = TolidSpecies(common_name="lugworm",
                                     family="Arenicolidae",
                                     genus="Arenicola",
                                     tax_order="None",
                                     phylum="Annelida",
                                     kingdom="Metazoa",
                                     prefix="wuAreMari",
                                     name="Arenicola marina",
                                     tax_class="Polychaeta",
                                     taxonomy_id=6344)
        db.session.add(self.species1)
        self.species2 = TolidSpecies(common_name="human",
                                     family="Hominidae",
                                     genus="Homo",
                                     tax_order="Primates",
                                     phylum="Chordata",
                                     kingdom="Metazoa",
                                     prefix="mHomSap",
                                     name="Homo sapiens",
                                     tax_class="Mammalia",
                                     taxonomy_id=9606)
        db.session.add(self.species2)
        self.species3 = TolidSpecies(common_name="None",
                                     family="Nereididae",
                                     genus="Perinereis",
                                     kingdom="Metazoa",
                                     tax_order="Phyllodocida",
                                     phylum="Annelida",
                                     prefix="wpPerVanc",
                                     name="Perinereis vancaurica",
                                     tax_class="Polychaeta",
                                     taxonomy_id=6355)
        db.session.add(self.species3)
        self.specimen1 = TolidSpecimen(specimen_id="SAN0000100",
                                       number=1, public_name="wuAreMari1")
        self.specimen1.species = self.species1
        self.specimen1.user = self.user1
        db.session.add(self.specimen1)
        # Another species for the same specimen
        self.specimen2 = TolidSpecimen(specimen_id="SAN0000101",
                                       number=2, public_name="wuAreMari2")
        self.specimen2.species = self.species1
        self.specimen2.user = self.user1
        db.session.add(self.specimen2)
        self.specimen3 = TolidSpecimen(specimen_id="SAN0000101",
                                       number=1, public_name="wpPerVanc1")
        self.specimen3.species = self.species3
        self.specimen3.user = self.user1
        db.session.add(self.specimen3)
        db.session.commit()
        db.engine.execute("ALTER SEQUENCE request_request_id_seq RESTART WITH 1;")

    def tearDown(self):
        db.session.query(TolidRequest).delete()
        db.session.query(TolidSpecimen).delete()
        db.session.query(TolidSpecies).delete()
        db.session.query(TolidRole).delete()
        db.session.query(TolidUser).delete()
        db.session.query(TolidState).delete()
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
