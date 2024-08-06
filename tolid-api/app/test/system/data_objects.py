# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from datetime import datetime

from sqlalchemy.orm import sessionmaker

from tol.core import DataSource

from ...main.model import (
    PrimaryPrefix,
    Request,
    SecondaryPrefix,
    Species,
    Specimen
)


def create_test_data(ds: DataSource, token: str):
    user1s = ds.insert(
        'user', [
            ds.data_object_factory(
                'user',
                '100',
                attributes={
                    'email': 'test@sanger.ac.uk',
                    'name': 'Test Creator User',
                    'organisation': 'Test Organisation'
                }
            ),
            ds.data_object_factory(
                'user',
                '200',
                attributes={
                    'email': 'test2@sanger.ac.uk',
                    'name': 'Test User',
                    'organisation': 'Test Organisation'
                }
            )
        ]
    )

    ds.insert(
        'token', [
            ds.data_object_factory(
                'token',
                None,
                attributes={
                    'token': token
                },
                to_one={
                    'user': user1s[0]
                },
            )
        ]
    )

    roles1s = ds.insert(
        'role', [
            ds.data_object_factory(
                'role',
                None,
                attributes={
                    'name': 'creator'
                }
            )
        ]
    )

    ds.insert(
        'role_binding', [
            ds.data_object_factory(
                'role_binding',
                None,
                to_one={
                    'role': roles1s[0],
                    'user': user1s[0]
                },
            )
        ]
    )
    species1s = ds.insert(
        'species', [
            ds.data_object_factory(
                'species',
                1234,
                attributes={
                    'name': 'Test Species',
                    'prefix': 'abCdeFghi',
                    'common_name': 'Test Common Name',
                    'genus': 'Test Genus',
                    'family': 'Test Family',
                    'tax_order': 'Test Order',
                    'tax_class': 'Test Class',
                    'phylum': 'Test Phylum',
                    'kingdom': 'Test Kingdom'
                }
            )
        ]
    )

    ds.insert(
        'specimen', [
            ds.data_object_factory(
                'specimen',
                'abCdeFghi1',
                attributes={
                    'specimen_id': 'TEST_SPECIMEN1',
                    'number': 1,
                    'requested_taxonomy_id': 5678,
                    'created_at': datetime.now()
                },
                to_one={
                    'species': species1s[0],
                    'user': user1s[1]
                }
            )
        ]
    )

    ds.insert(
        'request', [
            ds.data_object_factory(
                'request',
                None,
                attributes={
                    'specimen_id': 'TEST_SPECIMEN2',
                    'species_id': 1235,
                    'status': 'Pending',
                    'requested_taxonomy_id': 5678,
                    'created_at': datetime.now()
                },
                to_one={
                    'user': user1s[1]
                }
            )
        ]
    )


def delete_test_data(engine, auth_models):

    with sessionmaker(engine)() as session:
        session.query(Request).delete()
        session.query(Specimen).delete()
        session.query(Species).delete()
        session.query(auth_models.token_class).delete()
        session.query(auth_models.role_binding_class).delete()
        session.query(auth_models.role_class).delete()
        session.query(auth_models.user_class).delete()
        session.query(auth_models.state_class).delete()
        session.query(SecondaryPrefix).delete()
        session.query(PrimaryPrefix).delete()
        session.commit()
