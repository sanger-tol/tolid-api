from swagger_server.model import db, TolidSpecies, \
    TolidSpecimen, TolidUser, TolidRequest
from swagger_server.db_utils import create_request, \
    notify_requests_pending
from flask import jsonify
from sqlalchemy import or_
import connexion


def search_specimen(specimen_id=None, skip=None, limit=None):
    specimens = db.session.query(TolidSpecimen) \
        .filter(TolidSpecimen.specimen_id == specimen_id) \
        .all()

    if not specimens:
        return jsonify([])

    # This can be simplified once the model can be changed
    tolIds = []
    for specimen in specimens:
        tolId = {'tolId': specimen.public_name,
                 'species': specimen.species}
        tolIds.append(tolId)
    return jsonify([{'specimenId': specimen_id,
                    'tolIds': tolIds}])


def search_tol_id(tol_id=None, skip=None, limit=None):
    specimen = db.session.query(TolidSpecimen) \
        .filter(TolidSpecimen.public_name == tol_id) \
        .one_or_none()

    if specimen is None:
        return jsonify([])

    return jsonify([specimen])


def search_tol_id_by_taxon_specimen(taxonomy_id=None, specimen_id=None,
                                    skip=None, limit=None):
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


def search_species_by_taxon_prefix_name(taxonomy_id=None, prefix=None,
                                        scientific_name=None, skip=None, limit=None):
    if (taxonomy_id != "") and taxonomy_id.isnumeric():
        speciess = db.session.query(TolidSpecies) \
            .filter(or_(TolidSpecies.taxonomy_id == taxonomy_id,
                        TolidSpecies.prefix == prefix,
                        TolidSpecies.name == scientific_name)) \
            .order_by(TolidSpecies.taxonomy_id) \
            .all()
    else:
        speciess = db.session.query(TolidSpecies) \
            .filter(or_(TolidSpecies.prefix == prefix,
                        TolidSpecies.name == scientific_name)) \
            .order_by(TolidSpecies.taxonomy_id) \
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
            specimen = db.session.query(TolidSpecimen) \
                .filter(TolidSpecimen.species_id == taxonomy_id) \
                .filter(TolidSpecimen.specimen_id == specimen_id) \
                .one_or_none()
            if specimen is not None:
                db.session.rollback()
                return jsonify({'detail': "A ToLID already exists for specimenId " + specimen_id
                               + " and taxonomyId " + str(taxonomy_id)}), 400
            try:
                request = create_request(taxonomy_id, specimen_id, user)
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
