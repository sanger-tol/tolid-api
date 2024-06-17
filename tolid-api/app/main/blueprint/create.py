# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from flask import Blueprint, request

from tol.api_base2 import (
    custom_blueprint
)
from tol.api_base2.misc import (
    CtxGetter,
    default_ctx_getter
)
from tol.core import (
    DataSource,
    DataSourceFilter
)
from tol.core.data_source_dict import (
    DataSourceDict
)


def create_blueprint(
    *data_sources: DataSource,
    url_prefix: str = '/custom/create',
    ctx_getter: CtxGetter = default_ctx_getter
) -> Blueprint:

    create_blueprint = custom_blueprint(name='create',
                                             url_prefix=url_prefix)

    data_source_dict = DataSourceDict(*data_sources)

    @create_blueprint.route('/request', methods=['POST'])
    def create_request():
        data_source = data_source_dict['request']
        ctx = ctx_getter()
        user_id = ctx.user_id

        with data_source.get_session() as session:
            requests_to_upsert = []
            for row in request.json:
                species_id = row.get('species_taxonomy_id')
                specimen_id = row.get('specimen_id')
                # Does the request already exist?
                f = DataSourceFilter()
                f.and_ = {
                    'species_id': {'eq': {'value': species_id}},
                    'specimen_id': {'eq': {'value': specimen_id}}
                }
                existing_requests_count = session.get_count(
                    'request',
                    object_filters=f
                )
                if existing_requests_count > 0:
                    return {
                        'errors': [
                            {
                                'detail': f'Request already exists for {species_id}-{specimen_id}'
                            }
                        ]
                    }, 400

                # Does the ToLID already exist?
                f = DataSourceFilter()
                f.and_ = {
                    'species.id': {'eq': {'value': species_id}},
                    'specimen_id': {'eq': {'value': specimen_id}}
                }
                existing_tolids_count = session.get_count(
                    'specimen',
                    object_filters=f
                )
                if existing_tolids_count > 0:
                    return {
                        'errors': [
                            {
                                'detail': f'ToLID already exists for {species_id}-{specimen_id}'
                            }
                        ]
                    }, 400

                requests_to_upsert.append(
                    session.data_object_factory(
                        'request',
                        None,
                        attributes={
                            'species_id': species_id,
                            'requested_taxonomy_id': row.get('requested_taxonomy_id'),
                            'specimen_id': specimen_id,
                            'confirmation_name': row.get('species_name'),
                            'status': 'Pre-pending'
                        },
                        to_one={
                            'user': session.data_object_factory(
                                'user',
                                user_id
                            )
                        }
                    )
                )
            session.upsert('request', requests_to_upsert)
        return {}, 200

    return create_blueprint
