# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os
from dataclasses import dataclass

import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from tol.sql import create_session_factory
from tol.sql.session import SessionFactory

from main import application
import main.model as models


def __create_tables(db_uri: str) -> None:    
    engine = create_engine(db_uri)
    try:
        models.Base.metadata.create_all(engine)
    except Exception as e:
        print(e)


@dataclass(frozen=True)
class Data:
    user_requester: models.TolidUser
    user_admin: models.TolidUser
    user_creator: models.TolidUser
    user_requester2: models.TolidUser

    role1: models.TolidRole
    role2: models.TolidRole

    species1: models.TolidSpecies
    species2: models.TolidSpecies
    species3: models.TolidSpecies

    specimen1: models.TolidSpecimen
    specimen2: models.TolidSpecimen
    specimen3: models.TolidSpecimen


@pytest.fixture(scope='function')
def data(session: Session) -> Data:
    user_requester = models.TolidUser(
        user_id=100,
        name='test_user_requester',
        email='test_user_requester@sanger.ac.uk',
        organisation='Sanger Institute',
        api_key='AnyThingBecAuseThIsIsATEST123456'
    )
    session.add(user_requester)
    user_admin = models.TolidUser(
        user_id=200,
        name='test_user_admin',
        email='test_user_admin@sanger.ac.uk',
        organisation='Sanger Institute',
        api_key='AnyThingBecAuseThIsIsATEST567890'
    )
    session.add(user_admin)
    user_creator = models.TolidUser(
        user_id=300,
        name='test_user_creator',
        email='test_user_creator@sanger.ac.uk',
        organisation='Sanger Institute',
        api_key='AnyThingBecAuseThIsIsATEST24680'
    )
    user_requester2 = models.TolidUser(
        user_id=400,
        name='test_user_requester2',
        email='test_user_requester2@sanger.ac.uk',
        organisation='Sanger Institute',
        api_key='AnyThingBecAuseThIsIsATEST13579'
    )
    session.add(user_requester)
    session.add(user_admin)
    session.add(user_creator)
    session.add(user_requester2)
    role1 = models.TolidRole(role='admin')
    role1.user = user_admin
    session.add(role1)
    role2 = models.TolidRole(role='creator')
    role2.user = user_creator
    session.add(role2)
    species1 = models.TolidSpecies(
        common_name='lugworm',
        family='Arenicolidae',
        genus='Arenicola',
        tax_order='None',
        phylum='Annelida',
        kingdom='Metazoa',
        prefix='wuAreMari',
        name='Arenicola marina',
        tax_class='Polychaeta',
        taxonomy_id=6344
    )
    session.add(species1)
    species2 = models.TolidSpecies(
        common_name='human',
        family='Hominidae',
        genus='Homo',
        tax_order='Primates',
        phylum='Chordata',
        kingdom='Metazoa',
        prefix='mHomSap',
        name='Homo sapiens',
        tax_class='Mammalia',
        taxonomy_id=9606
    )
    session.add(species2)
    species3 = models.TolidSpecies(
        common_name='None',
        family='Nereididae',
        genus='Perinereis',
        kingdom='Metazoa',
        tax_order='Phyllodocida',
        phylum='Annelida',
        prefix='wpPerVanc',
        name='Perinereis vancaurica',
        tax_class='Polychaeta',
        taxonomy_id=6355
    )
    session.add(species3)
    specimen1 = models.TolidSpecimen(specimen_id='SAN0000100',
                                     number=1, tolid='wuAreMari1')
    specimen1.species = species1
    specimen1.user = user_requester
    session.add(specimen1)
    # Another species for the same specimen
    specimen2 = models.TolidSpecimen(specimen_id='SAN0000101',
                                     number=2, tolid='wuAreMari2')
    specimen2.species = species1
    specimen2.user = user_requester
    session.add(specimen2)
    specimen3 = models.TolidSpecimen(
        specimen_id='SAN0000101',
        number=1,
        tolid='wpPerVanc1'
    )
    specimen3.species = species3
    specimen3.user = user_requester
    session.add(specimen3)
    session.commit()

    return Data(
        user_admin=user_admin,
        user_creator=user_creator,
        user_requester=user_requester,
        user_requester2=user_requester2,
        role1=role1,
        role2=role2,
        species1=species1,
        species2=species2,
        species3=species3,
        specimen1=specimen1,
        specimen2=specimen2,
        specimen3=specimen3
    )


@pytest.fixture(scope='session', autouse=True)
def db_uri() -> str:
    uri = os.environ['DB_URI']
    __create_tables(uri)

    return uri


@pytest.fixture(scope='session')
def session_factory(db_uri: str) -> SessionFactory:
    return create_session_factory(db_uri)


@pytest.fixture(scope='function')
def session(session_factory: SessionFactory) -> Session:
    with session_factory() as sess:
        yield sess
        sess.execute(delete(models.TolidSpecimen))
        sess.execute(delete(models.TolidSpecies))
        sess.execute(delete(models.TolidRole))
        sess.execute(delete(models.TolidUser))
        sess.commit()


@pytest.fixture(scope='session')
def client():
    app = application()
    app.testing = True

    return app.test_client()
