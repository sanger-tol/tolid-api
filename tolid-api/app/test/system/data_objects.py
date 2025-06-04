# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from datetime import datetime
from typing import Iterator

from tol.core import OperableDataSource

SUBSPECIES_ID = 3102645
SPECIES_ID = 4039
SPECIES_NOT_EXISTS_ID = 37657


def create_test_data(ds: OperableDataSource, token: str):
    user1s = list(
        ds.insert(
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

    roles1s = list(
        ds.insert(
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
    species1s = list(
        ds.insert(
            'species', [
                ds.data_object_factory(
                    'species',
                    SPECIES_ID,
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
    )

    ds.insert(
        'specimen', [
            ds.data_object_factory(
                'specimen',
                'abCdeFghi1',
                attributes={
                    'specimen_id': 'TEST_SPECIMEN1',
                    'number': 1,
                    'requested_taxonomy_id': SUBSPECIES_ID,
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
                    'species_id': SPECIES_NOT_EXISTS_ID,
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


def delete_test_data(sql_ds: OperableDataSource, auth_models):

    delete_order = [
        'request',
        'specimen',
        'species',
        'token',
        'role_binding',
        'role',
        'user',
        'oidc_state',
        'secondary_prefix',
        'primary_prefix',
    ]

    def __get_ids(object_type: str) -> Iterator[str]:
        return (
            o.id
            for o
            in sql_ds.get_list(object_type)
        )

    for object_type in delete_order:
        ids = list(__get_ids(object_type))

        sql_ds.delete(
            object_type,
            ids,
        )
