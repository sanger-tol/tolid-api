# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import logging
import os
from datetime import datetime, timedelta

import connexion

from flask_testing import TestCase

from main.encoder import JSONEncoder
from main.model import TolidPrimaryPrefix, TolidRequest, TolidRole, \
    TolidRoleBinding, \
    TolidSecondaryPrefix, TolidSpecies, TolidSpecimen, TolidState, \
    TolidToken, TolidUser, db


class BaseTestCase(TestCase):

    def setUp(self):
        far_future = datetime.now() + timedelta(days=2000)

        self.maxDiff = None
        db.create_all()
        self.user1 = TolidUser(id=100,
                               name='test_user_requester',
                               email='test_user_requester@sanger.ac.uk',
                               workplace='Sanger Institute')
        self.token1 = TolidToken(
            id=100,
            token='AnyThingBecAuseThIsIsATEST123456',
            expires_at=far_future,
            user_id=100
        )
        db.session.add(self.user1)
        db.session.add(self.token1)

        self.user2 = TolidUser(id=200,
                               name='test_user_admin',
                               email='test_user_admin@sanger.ac.uk',
                               workplace='Sanger Institute')
        self.token2 = TolidToken(
            id=200,
            token='AnyThingBecAuseThIsIsATEST567890',
            expires_at=far_future,
            user_id=200
        )
        db.session.add(self.user2)
        db.session.add(self.token2)

        self.user3 = TolidUser(id=300,
                               name='test_user_creator',
                               email='test_user_creator@sanger.ac.uk',
                               workplace='Sanger Institute')
        self.token3 = TolidToken(
            id=300,
            token='AnyThingBecAuseThIsIsATEST24680',
            expires_at=far_future,
            user_id=300
        )
        db.session.add(self.user3)
        db.session.add(self.token3)

        self.user4 = TolidUser(id=400,
                               name='test_user_requester2',
                               email='test_user_requester2@sanger.ac.uk',
                               workplace='Sanger Institute')
        self.token4 = TolidToken(
            id=400,
            token='AnyThingBecAuseThIsIsATEST13579',
            expires_at=far_future,
            user_id=400
        )
        db.session.add(self.user4)
        db.session.add(self.token4)

        self.role1 = TolidRole(id=1, name='admin')
        db.session.add(self.role1)
        self.role2 = TolidRole(id=2, name='creator')
        db.session.add(self.role2)

        self.role_binding1 = TolidRoleBinding(
            user_id=200,
            role_id=1
        )
        db.session.add(self.role_binding1)
        self.role_binding2 = TolidRoleBinding(
            user_id=300,
            role_id=2
        )
        db.session.add(self.role_binding2)

        self.species1 = TolidSpecies(common_name='lugworm',
                                     family='Arenicolidae',
                                     genus='Arenicola',
                                     tax_order='None',
                                     phylum='Annelida',
                                     kingdom='Metazoa',
                                     prefix='wuAreMari',
                                     name='Arenicola marina',
                                     tax_class='Polychaeta',
                                     taxonomy_id=6344)
        db.session.add(self.species1)
        self.species2 = TolidSpecies(common_name='human',
                                     family='Hominidae',
                                     genus='Homo',
                                     tax_order='Primates',
                                     phylum='Chordata',
                                     kingdom='Metazoa',
                                     prefix='mHomSap',
                                     name='Homo sapiens',
                                     tax_class='Mammalia',
                                     taxonomy_id=9606)
        db.session.add(self.species2)
        self.species3 = TolidSpecies(common_name='None',
                                     family='Nereididae',
                                     genus='Perinereis',
                                     kingdom='Metazoa',
                                     tax_order='Phyllodocida',
                                     phylum='Annelida',
                                     prefix='wpPerVanc',
                                     name='Perinereis vancaurica',
                                     tax_class='Polychaeta',
                                     taxonomy_id=6355)
        db.session.add(self.species3)
        self.specimen1 = TolidSpecimen(specimen_id='SAN0000100',
                                       number=1, tolid='wuAreMari1')
        self.specimen1.species = self.species1
        self.specimen1.user = self.user1
        db.session.add(self.specimen1)
        # Another species for the same specimen
        self.specimen2 = TolidSpecimen(specimen_id='SAN0000101',
                                       number=2, tolid='wuAreMari2')
        self.specimen2.species = self.species1
        self.specimen2.user = self.user1
        db.session.add(self.specimen2)
        self.specimen3 = TolidSpecimen(specimen_id='SAN0000101',
                                       number=1, tolid='wpPerVanc1')
        self.specimen3.species = self.species3
        self.specimen3.user = self.user1
        db.session.add(self.specimen3)
        db.session.commit()
        db.engine.execute('ALTER SEQUENCE request_request_id_seq RESTART WITH 1;')

    def tearDown(self):
        db.session.query(TolidRequest).delete()
        db.session.query(TolidSpecimen).delete()
        db.session.query(TolidSpecies).delete()
        db.session.query(TolidToken).delete()
        db.session.query(TolidRoleBinding).delete()
        db.session.query(TolidRole).delete()
        db.session.query(TolidUser).delete()
        db.session.query(TolidState).delete()
        db.session.query(TolidSecondaryPrefix).delete()
        db.session.query(TolidPrimaryPrefix).delete()
        db.session.commit()

    def create_app(self):
        logging.getLogger('connexion').setLevel('ERROR')
        logging.getLogger('openapi_spec_validator').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='/app/main/swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml', pythonic_params=True)
        app.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
        app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app.app)
        return app.app
