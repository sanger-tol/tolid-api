# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from main.model import db, TolidSpecies, \
    TolidSpecimen, TolidUser, TolidRequest, TolidPrimaryPrefix
from main.db_utils import create_request, \
    notify_requests_pending
from flask import jsonify
from sqlalchemy import or_
import connexion
import os
import logging


DEFAULT_MAX_SPECIES_RETURNED = 50


def search_specimen(specimen_id=None, skip=None, limit=None):
    specimens = db.session.query(TolidSpecimen) \
        .filter(TolidSpecimen.specimen_id == specimen_id) \
        .all()

    if not specimens:
        return jsonify({'detail': "Specimen with ID " + specimen_id
                       + " cannot be found"}), 404

    # This can be simplified once the model can be changed
    tolIds = []
    for specimen in specimens:
        tolId = {'tolId': specimen.tolid,
                 'species': specimen.species}
        tolIds.append(tolId)
    return jsonify([{'specimenId': specimen_id,
                    'tolIds': tolIds}])


def search_tol_id(tol_id=None, skip=None, limit=None):
    specimen = db.session.query(TolidSpecimen) \
        .filter(TolidSpecimen.tolid == tol_id) \
        .one_or_none()

    if specimen is None:
        return jsonify([])

    return jsonify([specimen])


def search_tol_id_by_taxon_specimen(taxonomy_id=None, specimen_id=None,
                                    skip=None, limit=None):
    if not taxonomy_id.isnumeric():
        return jsonify({'detail': "taxonomyId must be an integer"}), 404

    specimen = db.session.query(TolidSpecimen) \
        .filter(TolidSpecimen.species_id == taxonomy_id) \
        .filter(TolidSpecimen.specimen_id == specimen_id) \
        .one_or_none()

    if specimen is None:
        return jsonify([])

    return jsonify([specimen])


def tol_ids_for_user(api_key=None):
    specimens = db.session.query(TolidSpecimen) \
        .filter(TolidSpecimen.created_by == connexion.context["user"]) \
        .order_by(TolidSpecimen.created_at.desc()) \
        .all()
    return jsonify(specimens)


def search_species(taxonomy_id=None, skip=None, limit=None):
    if not taxonomy_id.isnumeric():
        return jsonify({'detail': "Species with taxonomyId " + str(taxonomy_id)
                       + " cannot be found"}), 404

    species = db.session.query(TolidSpecies) \
        .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
        .one_or_none()

    if species is None:
        return jsonify({'detail': "Species with taxonomyId " + str(taxonomy_id)
                       + " cannot be found"}), 404

    return jsonify([species.to_long_dict()])


def search_species_by_taxon_prefix_genus(taxonomy_id=None, prefix=None,
                                        genus=None, output=None):
    query = db.session.query(TolidSpecies)
    filters = []
    if prefix is not None:
        filters.append(TolidSpecies.prefix == prefix)
    if taxonomy_id is not None:
        if (taxonomy_id != "") and taxonomy_id.isnumeric():
            # Valid integer taxonomy ID
            filters.append(TolidSpecies.taxonomy_id == taxonomy_id)
        else:
            # Force this filter to fail
            filters.append(TolidSpecies.taxonomy_id == TolidSpecies.taxonomy_id + 1)
    if genus is not None:
        filters.append(TolidSpecies.genus == genus)

    if len(filters) == 0:
        return jsonify([])
    else:
        query = query.filter(or_(*filters))

    speciess = query.order_by(TolidSpecies.taxonomy_id).all()

    return jsonify([species.to_long_dict() for species in speciess])


def search_species_by_scientific_name(scientific_name_fragment, page=0):
    if scientific_name_fragment.isspace():
        return jsonify({'detail': 'A section of a scientific name is needed'}), 400
    
    max_species = os.getenv(
        "MAX_SPECIES_RETURNED",
        DEFAULT_MAX_SPECIES_RETURNED
    )

    formatted = "%{}%".format(scientific_name_fragment)

    speciess = db.session.query(TolidSpecies) \
        .filter(TolidSpecies.name.ilike(formatted)) \
        .order_by(TolidSpecies.name) \
        .offset(page * max_species) \
        .limit((page + 1) * max_species) \
        .all()

    return jsonify([species.to_long_dict() for species in speciess])


def requests_for_user(api_key=None):
    requests = db.session.query(TolidRequest) \
        .filter(TolidRequest.created_by == connexion.context["user"]) \
        .order_by(TolidRequest.created_at.desc()) \
        .all()
    return jsonify(requests)


def bulk_add_requests(body=None, api_key=None):
    user = db.session.query(TolidUser) \
        .filter(TolidUser.user_id == connexion.context["user"]) \
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
            specimen = db.session.query(TolidSpecimen) \
                .filter(TolidSpecimen.species_id == taxonomy_id) \
                .filter(TolidSpecimen.specimen_id == specimen_id) \
                .one_or_none()
            if specimen is not None:
                db.session.rollback()
                return jsonify({'detail': "A ToLID already exists for specimenId " + specimen_id
                               + " and taxonomyId " + str(taxonomy_id)}), 400
            try:
                request = create_request(taxonomy_id, specimen_id, user, confirmation_name)
            except Exception as e:
                # Another user created a request
                db.session.rollback()
                return jsonify({'detail': str(e)}), 400

            requests.append(request)
            db.session.add(request)
        notify_requests_pending()
        db.session.commit()

    return jsonify(requests)


def search_request(request_id=None, skip=None, limit=None):
    request = db.session.query(TolidRequest) \
        .filter(TolidRequest.request_id == request_id) \
        .one_or_none()

    if request is None:
        return jsonify([])

    return jsonify([request])


def retrieve_prefixes():
    primary_prefixes = db.session.query(TolidPrimaryPrefix) \
       .order_by(TolidPrimaryPrefix.letter) \
       .all()
    return jsonify(primary_prefixes)


def list_assigned_tolid_species(page=None):
    # pages work like indexes & 50 species to a page
    page = int(page)
    species = db.session.query(TolidSpecies) \
        .join(TolidSpecimen) \
        .order_by(TolidSpecies.name) \
        .offset((page*50)+1) \
        .limit((page+1)*50) \
        .all()

    return jsonify([individual.to_long_dict() for individual in species])


def get_environment():
    deployment_environment = os.getenv("ENVIRONMENT")
    if deployment_environment is not None and deployment_environment != "":
        return jsonify({'environment': deployment_environment})

    # if unset, assume dev
    logging.warn("$ENVIRONMENT is unset - assuming a 'dev' environment")
    return jsonify({'environment': 'dev'})
