# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import logging
import os

from flask import jsonify

from tol.api_base2.misc import default_ctx_getter

from main.db_utils import create_request, \
    notify_requests_pending
from main.model import TolidPrimaryPrefix, TolidRequest, TolidSpecies, \
    TolidSpecimen, TolidUser, session_factory

from sqlalchemy import or_



def search_specimen(specimen_id=None, skip=None, limit=None):
    with session_factory() as session:
        specimens = session.query(TolidSpecimen) \
            .filter(TolidSpecimen.specimen_id == specimen_id) \
            .all()

        if not specimens:
            return jsonify({'detail': f'Specimen with ID {specimen_id}'
                            ' cannot be found'}), 404

        # This can be simplified once the model can be changed
        tolids = []
        for specimen in specimens:
            tolid = {'tolId': specimen.tolid,
                    'species': specimen.species,
                    'user': specimen.user}
            tolids.append(tolid)
        return jsonify([{'specimenId': specimen_id,
                        'tolIds': tolids}])


def search_tol_id(tol_id=None, skip=None, limit=None):
    with session_factory() as session:
        specimen = session.query(TolidSpecimen) \
            .filter(TolidSpecimen.tolid == tol_id) \
            .one_or_none()

        if specimen is None:
            return jsonify([])

        return jsonify([specimen])


def search_tol_id_by_taxon_specimen(taxonomy_id: str = None, specimen_id=None,
                                    skip=None, limit=None):
    with session_factory() as session:
        if not taxonomy_id.isnumeric():
            return jsonify({'detail': 'taxonomyId must be an integer'}), 404

        specimen = session.query(TolidSpecimen) \
            .filter(TolidSpecimen.species_id == taxonomy_id) \
            .filter(TolidSpecimen.specimen_id == specimen_id) \
            .one_or_none()

        if specimen is None:
            return jsonify([])

        return jsonify([specimen])


def tol_ids_for_user():
    with session_factory() as session:
        specimens = session.query(TolidSpecimen) \
            .filter(TolidSpecimen.created_by == default_ctx_getter().user_id) \
            .order_by(TolidSpecimen.created_at.desc()) \
            .all()
        return jsonify(specimens)


def search_species(taxonomy_id: str = None, skip=None, limit=None):
    if not taxonomy_id.isnumeric():
        return jsonify({'detail': f'Species with taxonomyId {taxonomy_id}'
                        ' cannot be found'}), 404

    with session_factory() as session:
        species = session.query(TolidSpecies) \
            .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
            .one_or_none()

        if species is None:
            return jsonify({'detail': f'Species with taxonomyId {taxonomy_id}'
                            ' cannot be found'}), 404

        return jsonify([species.to_long_dict()])


def search_species_by_search_term(taxonomy_id=None, prefix=None,
                                  genus=None, scientific_name_fragment=None,
                                  page=0, output=None):
    with session_factory() as session:
        query = session.query(TolidSpecies)
        filters = []
        if prefix is not None:
            filters.append(TolidSpecies.prefix == prefix)
        if taxonomy_id is not None:
            if (taxonomy_id != '') and taxonomy_id.isnumeric():
                # Valid integer taxonomy ID
                filters.append(TolidSpecies.taxonomy_id == taxonomy_id)
            else:
                # Force this filter to fail
                filters.append(TolidSpecies.taxonomy_id == TolidSpecies.taxonomy_id + 1)
        if genus is not None:
            filters.append(TolidSpecies.genus == genus)
        if scientific_name_fragment is not None:
            filters.append(TolidSpecies.name.ilike(f'%{scientific_name_fragment}%'))

        if len(filters) == 0:
            return jsonify({
                'totalNumSpecies': 0,
                'species': []
            })
        else:
            query = query.filter(or_(*filters))

        max_species_per_page = 50

        total_num_species = query.count()

        speciess = query.order_by(TolidSpecies.taxonomy_id) \
                        .offset(page * max_species_per_page) \
                        .limit(max_species_per_page) \
                        .all()

        return jsonify({
            'totalNumSpecies': total_num_species,
            'species': [species.to_long_dict() for species in speciess]
        })


def requests_for_user():
    with session_factory() as session:
        requests = session.query(TolidRequest) \
            .filter(TolidRequest.created_by == connexion.context['user']) \
            .order_by(TolidRequest.created_at.desc()) \
            .all()
        return jsonify(requests)


def bulk_add_requests(body=None):
    with session_factory() as session:
        user = session.query(TolidUser) \
            .filter(TolidUser.user_id == default_ctx_getter().user_id) \
            .one_or_none()
        requests = []
        # body contains the rows of data
        if body:
            for row in body:
                specimen_id = row['specimenId']
                taxonomy_id = row['taxonomyId']
                if 'confirmationName' in row:
                    confirmation_name = row['confirmationName']
                else:
                    confirmation_name = None
                specimen = session.query(TolidSpecimen) \
                    .filter(TolidSpecimen.species_id == taxonomy_id) \
                    .filter(TolidSpecimen.specimen_id == specimen_id) \
                    .one_or_none()
                if specimen is not None:
                    session.rollback()
                    return jsonify({'detail': f'A ToLID already exists for specimenId {specimen_id}'
                                    f' and taxonomyId {taxonomy_id}'}), 400
                try:
                    request = create_request(taxonomy_id, specimen_id, user, confirmation_name)
                except Exception as e:
                    # Another user created a request
                    session.rollback()
                    return jsonify({'detail': str(e)}), 400

                requests.append(request)
                session.add(request)
            notify_requests_pending()
            session.commit()

        return jsonify(requests)


def search_request(request_id=None, skip=None, limit=None):
    with session_factory() as session:
        request = session.query(TolidRequest) \
            .filter(TolidRequest.request_id == request_id) \
            .one_or_none()

        if request is None:
            return jsonify([])

        return jsonify([request])


def retrieve_prefixes():
    with session_factory() as session:
        primary_prefixes = session.query(TolidPrimaryPrefix) \
            .order_by(TolidPrimaryPrefix.letter) \
            .all()
        return jsonify(primary_prefixes)


def list_assigned_tolid_species(page=None):
    with session_factory() as session:
        # pages work like indexes & 50 species to a page
        page = int(page)
        species = session.query(TolidSpecies) \
            .join(TolidSpecimen) \
            .order_by(TolidSpecies.name) \
            .offset(page * 50) \
            .limit(50) \
            .all()

        return jsonify([individual.to_long_dict() for individual in species])


def get_environment():
    deployment_environment = os.getenv('ENVIRONMENT')
    if deployment_environment is not None and deployment_environment != '':
        return jsonify({'environment': deployment_environment})

    # if unset, assume dev
    logging.warn('$ENVIRONMENT is unset - assuming a "dev" environment')
    return jsonify({'environment': 'dev'})
