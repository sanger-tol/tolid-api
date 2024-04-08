# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from flask import jsonify

from tol.api_base2.misc import default_ctx_getter
from tol.sql import create_session_factory

from main.controllers.auth import require_creator
from main.db_utils import create_new_specimen, \
    create_request, notify_requests_pending
from main.model import TolidRequest, TolidSpecies, \
    TolidSpecimen, TolidUser, session_factory


@require_creator
def add_specimen(taxonomy_id=None, specimen_id=None):
    """adds a specimen and assigns a ToLID

    Adds a new ToLID to the system

    :param taxonomy_id: valid NCBI Taxonomy identifier
    :type taxonomy_id: str
    :param specimen_id: valid GAL specimen identifier
    :type specimen_id: str

    :return: JSON with complete ToLID and taxa structure
    """

    with session_factory() as session:
        user = session.query(TolidUser) \
            .filter(TolidUser.user_id == default_ctx_getter().user_id) \
            .one_or_none()
        species = session.query(TolidSpecies) \
            .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
            .one_or_none()

        if species is None:
            return jsonify({'detail': f'Species with taxonomyId {taxonomy_id}'
                            ' cannot be found'}), 400

        specimen = session.query(TolidSpecimen) \
            .filter(TolidSpecimen.specimen_id == specimen_id) \
            .filter(TolidSpecimen.species_id == taxonomy_id) \
            .one_or_none()

        if specimen is None:
            specimen = create_new_specimen(species, specimen_id, user)
            session.add(specimen)
            session.commit()

        return jsonify([specimen])


@require_creator
def bulk_search_specimens(body=None):

    with session_factory() as session:
        user = session.query(TolidUser) \
            .filter(TolidUser.user_id == default_ctx_getter().user_id) \
            .one_or_none()
        results = []
        # body contains the rows of data
        if body:
            for row in body:
                specimen_id = row['specimenId']
                taxonomy_id = row['taxonomyId']
                species = session.query(TolidSpecies) \
                    .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
                    .one_or_none()

                if species is None:
                    # The species is not in the database - create a request for it if needed
                    request = session.query(TolidRequest) \
                        .filter(TolidRequest.species_id == taxonomy_id) \
                        .filter(TolidRequest.specimen_id == specimen_id) \
                        .one_or_none()
                    if request is None:
                        # We won't get an exception from the following because we've checked first
                        request = create_request(taxonomy_id, specimen_id, user)
                        session.add(request)
                    results.append(request)
                else:
                    # Species is in the database - create specimen for it if needed
                    specimen = session.query(TolidSpecimen) \
                        .filter(TolidSpecimen.species_id == taxonomy_id) \
                        .filter(TolidSpecimen.specimen_id == specimen_id) \
                        .one_or_none()

                    if specimen is None:
                        specimen = create_new_specimen(species, specimen_id, user)
                        session.add(specimen)

                    results.append(specimen)
            notify_requests_pending()
            session.commit()

        return jsonify(results)
