# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from datetime import datetime

from flask import Blueprint, request

from tol.api_base2 import (
    custom_blueprint
)
from tol.api_base2.auth import (
    require_auth
)
from tol.api_base2.misc import (
    CtxGetter,
    default_ctx_getter
)
from tol.api_client2.view import (
    DefaultView
)
from tol.core import (
    DataSource,
    DataSourceFilter
)
from tol.core.data_source_dict import (
    DataSourceDict
)


def request_blueprint(
    *data_sources: DataSource,
    url_prefix: str = '/custom/request',
    ctx_getter: CtxGetter = default_ctx_getter
) -> Blueprint:

    request_blueprint = custom_blueprint(
        name='create',
        url_prefix=url_prefix
    )

    data_source_dict = DataSourceDict(*data_sources)
    view = DefaultView(
        prefix='',
        include_all_to_ones=True,
        hop_limit=1
    )

    @request_blueprint.route('/create', methods=['POST'])
    @require_auth
    def create_request():
        data_source = data_source_dict['request']
        ctx = ctx_getter()
        user_id = ctx.user_id

        with data_source.get_session() as session:
            requests_to_insert = []
            for row in request.json:
                species_id = row.get('species_id')
                requested_taxonomy_id = row.get('requested_taxonomy_id')
                specimen_id = row.get('specimen_id')
                species_name = row.get('species_name')

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

                requests_to_insert.append(
                    session.data_object_factory(
                        'request',
                        None,
                        attributes={
                            'species_id': species_id,
                            'requested_taxonomy_id': requested_taxonomy_id,
                            'specimen_id': specimen_id,
                            'confirmation_name': species_name,
                            'status': 'Pre-pending',
                            'created_at': datetime.now(),
                        },
                        to_one={
                            'user': session.get_one(
                                'user',
                                user_id
                            )
                        }
                    )
                )
            requests_inserted = session.insert('request', requests_to_insert)
        return view.dump_bulk(requests_inserted), 200

    @request_blueprint.route('/reject', methods=['PATCH'])
    @require_auth(role='admin')
    def reject_request():
        data_source = data_source_dict['request']

        with data_source.get_session() as session:
            requests_to_upsert = []
            for row in request.json:
                request_id = row.get('request_id')
                reason = row.get('reason')

                tolid_request = session.get_one('request', request_id)
                if tolid_request is None:
                    return {
                        'errors': [
                            {
                                'detail': f'Request {request_id} does not exist'
                            }
                        ]
                    }, 400

                requests_to_upsert.append(
                    session.data_object_factory(
                        'request',
                        request_id,
                        attributes={
                            'status': 'Rejected',
                            'reason': reason,
                        }
                    )
                )
            requests_upserted = session.upsert('request', requests_to_upsert)
        return view.dump_bulk(requests_upserted), 200

    return request_blueprint
