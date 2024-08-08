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

from ..util import create_new_tolid


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
    @require_auth(ctx_getter=ctx_getter)
    def create_request():
        ctx = ctx_getter()
        user_id = ctx.user_id
        roles = ctx.roles
        errors = __validate_taxonomy_ids(request)
        if len(errors) > 0:
            return {
                'errors': errors
            }, 400
        if 'creator' in roles:
            return __create_request_creator(user_id, request)
        else:
            return __create_request_user(user_id, request)

    def __validate_taxonomy_ids(request):
        errors = []
        data_source_species = data_source_dict['species']
        data_source_taxon = data_source_dict['taxon']
        for row in request.json:
            requested_taxonomy_id = row.get('requested_taxonomy_id')
            specimen_id = row.get('specimen_id')

            if requested_taxonomy_id is None:
                errors.append(
                    {
                        'detail': 'requested_taxonomy_id is required'
                    }
                )
            if specimen_id is None:
                errors.append(
                    {
                        'detail': 'specimen_id is required'
                    }
                )

            # Is the requested_species in the ToLID database? If so, validation complete
            species_in_db = data_source_species.get_one('species', requested_taxonomy_id)
            print(f'GetOne {species_in_db}')
            if species_in_db is not None:
                print(f'Found in ToLID {requested_taxonomy_id} {species_in_db.id}')
                continue

            # If we are here, we need to check this species with GoaT
            requested_species = data_source_taxon.get_one('taxon', requested_taxonomy_id)
            if requested_species is None:
                errors.append(
                    {
                        'detail': f'Requested taxonomy {requested_taxonomy_id} does not exist'
                    }
                )
            if requested_species.rank not in ['species', 'subspecies']:
                errors.append(
                    {
                        'detail': f'{requested_taxonomy_id} is not of rank species or subspecies'
                    }
                )

        return errors

    def __get_species_id(requested_taxonomy_id, data_source_taxon, session):
        species_in_db = session.get_one('species', requested_taxonomy_id)
        print(f'GetOne {requested_taxonomy_id} {species_in_db}')
        if species_in_db is None:
            taxon = data_source_taxon.get_one('taxon', requested_taxonomy_id)
            species_id = int(taxon.species.id)
            print('FROM GOAT')
        else:
            species_id = species_in_db.id
            print('FROM TOLID')
        print(species_id)
        return species_id

    def __create_request_user(user_id, request):
        data_source = data_source_dict['request']
        data_source_taxon = data_source_dict['taxon']
        with data_source.get_session() as session:
            requests_to_insert = []
            errors = []
            for row in request.json:
                requested_taxonomy_id = row.get('requested_taxonomy_id')
                species_id = __get_species_id(requested_taxonomy_id, data_source_taxon, session)
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
                    errors.append(
                        {
                            'detail': f'Request already exists for {species_id}-{specimen_id}'
                        }
                    )
                    continue

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
                    errors.append(
                        {
                            'detail': f'ToLID already exists for {species_id}-{specimen_id}'
                        }
                    )
                    continue
                requests_to_insert.append(
                    session.data_object_factory(
                        'request',
                        None,
                        attributes={
                            'species_id': species_id,
                            'requested_taxonomy_id': requested_taxonomy_id,
                            'specimen_id': specimen_id,
                            'confirmation_name': species_name,
                            'status': 'Pending',
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
                print(f'GetOneUser {user_id}')
            if len(errors) > 0:
                return {
                    'errors': errors
                }, 400
            requests_inserted = session.insert('request', requests_to_insert)
        return view.dump_bulk(requests_inserted), 200

    def __create_request_creator(user_id, request):
        data_source = data_source_dict['specimen']
        data_source_taxon = data_source_dict['taxon']
        with data_source.get_session() as session:
            ret = []
            for row in request.json:
                requested_taxonomy_id = row.get('requested_taxonomy_id')
                species_id = __get_species_id(requested_taxonomy_id, data_source_taxon, session)
                specimen_id = row.get('specimen_id')
                species_name = row.get('species_name')
                print(f'{species_id} {specimen_id} {species_name}')
                # Does the species exist in the ToLID database?
                species = session.get_one('species', species_id)
                print(f'GetOne {species_id} {species}')
                if species is not None:
                    print('Found in ToLID')
                    # Does the tolid already exist?
                    f = DataSourceFilter()
                    f.and_ = {
                        'species_id': {'eq': {'value': species_id}},
                        'specimen_id': {'eq': {'value': specimen_id}}
                    }
                    existing_tolids = list(session.get_list(
                        'specimen',
                        object_filters=f
                    ))
                    if len(existing_tolids) > 0:
                        ret.extend(existing_tolids)
                        continue

                    ret.extend(
                        session.insert('specimen', [
                            create_new_tolid(
                                session,
                                species,
                                specimen_id,
                                requested_taxonomy_id,
                                session.get_one(
                                    'user',
                                    user_id
                                )
                            )
                        ])
                    )
                else:
                    # Species does not exist

                    # Does the request already exist?
                    f = DataSourceFilter()
                    f.and_ = {
                        'species_id': {'eq': {'value': species_id}},
                        'specimen_id': {'eq': {'value': specimen_id}}
                    }
                    existing_requests = list(session.get_list(
                        'request',
                        object_filters=f
                    ))
                    if len(existing_requests) > 0:
                        ret.extend(existing_requests)
                        continue
                    ret.extend(
                        session.insert('request', [
                            session.data_object_factory(
                                'request',
                                None,
                                attributes={
                                    'species_id': species_id,
                                    'requested_taxonomy_id': requested_taxonomy_id,
                                    'specimen_id': specimen_id,
                                    'confirmation_name': species_name,
                                    'status': 'Pending',
                                    'created_at': datetime.now(),
                                },
                                to_one={
                                    'user': session.get_one(
                                        'user',
                                        user_id
                                    )
                                }
                            )
                        ])
                    )
        return view.dump_bulk(ret), 200

    @request_blueprint.route('/reject', methods=['PATCH'])
    @require_auth(role='admin', ctx_getter=ctx_getter)
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

    @request_blueprint.route('/accept', methods=['PATCH'])
    @require_auth(role='admin', ctx_getter=ctx_getter)
    def accept_request():
        data_source = data_source_dict['request']

        with data_source.get_session() as session:
            tolids_inserted = []
            for row in request.json:
                request_id = row.get('request_id')

                tolid_request = session.get_one('request', request_id)
                if tolid_request is None:
                    return {
                        'errors': [
                            {
                                'detail': f'Request {request_id} does not exist'
                            }
                        ]
                    }, 400

                species = session.get_one('species', tolid_request.species_id)
                if species is None:
                    return {
                        'errors': [
                            {
                                'detail': f'Species {tolid_request.species_id} does not exist'
                            }
                        ]
                    }, 400

                tolids_inserted.extend(
                    session.insert('specimen', [
                        create_new_tolid(
                            session,
                            species,
                            tolid_request.specimen_id,
                            tolid_request.requested_taxonomy_id,
                            tolid_request.user
                        )
                    ])
                )
                session.delete('request', [tolid_request.id])
        return view.dump_bulk(tolids_inserted), 200

    return request_blueprint
