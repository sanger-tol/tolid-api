# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from Bio import Entrez

import connexion

from flask import jsonify

from main.db_utils import accept_request, reject_request
from main.model import TolidRequest, TolidRole, TolidSpecies, TolidSpecimen, db


def add_species(body=None, api_key=None):
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403

    species = db.session.query(TolidSpecies) \
        .filter(TolidSpecies.taxonomy_id == body['taxonomyId']) \
        .one_or_none()
    if species is not None:
        return jsonify({'detail': 'Species with taxonomyId ' + str(body['taxonomyId'])
                        + ' already exists'}), 400

    species = TolidSpecies()
    species.prefix = body['prefix']
    species.name = body['scientificName']
    species.taxonomy_id = body['taxonomyId']
    species.common_name = body['commonName']
    species.genus = body['genus']
    species.family = body['family']
    species.prefix = body['prefix']
    species.tax_order = body['order']
    species.tax_class = body['taxaClass']
    species.phylum = body['phylum']
    species.kingdom = body['kingdom']

    db.session.add(species)
    db.session.commit()

    return jsonify([species.to_long_dict()])


def edit_species(taxonomy_id=None, body=None, api_key=None):
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403

    if not taxonomy_id.isnumeric():
        return 'taxonomyId should be numeric', 404

    species = db.session.query(TolidSpecies) \
        .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
        .one_or_none()
    if species is None:
        return jsonify({'detail': 'Species with taxonomyId ' + str(taxonomy_id)
                       + ' cannot be found'}), 404

    species.prefix = body['prefix']
    species.name = body['scientificName']
    # Don't allow the taxonomy ID to be changed
    # species.taxonomy_id=body["taxonomyId"]
    species.common_name = body['commonName']
    species.genus = body['genus']
    species.family = body['family']
    species.prefix = body['prefix']
    species.tax_order = body['order']
    species.tax_class = body['taxaClass']
    species.phylum = body['phylum']
    species.kingdom = body['kingdom']

    db.session.commit()

    return jsonify([species.to_long_dict()])


def list_specimens(taxonomy_id=None, skip=None, limit=None):
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403

    if taxonomy_id is None:
        specimens = db.session.query(TolidSpecimen) \
            .order_by(TolidSpecimen.species_id) \
            .order_by(TolidSpecimen.specimen_id) \
            .order_by(TolidSpecimen.number) \
            .all()
    else:
        species = db.session.query(TolidSpecies) \
            .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
            .one_or_none()

        if species is None:
            return jsonify({'detail': 'Species with taxonomyId ' + str(taxonomy_id)
                           + ' cannot be found'}), 400

        specimens = db.session.query(TolidSpecimen) \
            .filter(TolidSpecimen.species_id == taxonomy_id) \
            .order_by(TolidSpecimen.specimen_id) \
            .order_by(TolidSpecimen.number) \
            .all()

    output = ''
    for specimen in specimens:
        output += specimen.tolid + '\t' + specimen.species.name + '\t' \
            + specimen.specimen_id + '\t' + str(specimen.number) + '\n'
    return output.strip()


def list_species():
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403

    speciess = db.session.query(TolidSpecies).order_by(TolidSpecies.taxonomy_id).all()

    if 'accept' in connexion.request.headers \
            and str(connexion.request.headers['accept']).startswith('text/plain'):
        # Set Content-Type header
        output = ''
        for species in speciess:
            output += species.prefix + '\t' + species.name + '\t' + str(species.taxonomy_id) \
                + '\t' + species.common_name + '\t' + species.genus + '\t' + species.family \
                + '\t' + species.tax_order + '\t' + species.tax_class + '\t' + species.phylum \
                + '\n'
        return connexion.lifecycle.ConnexionResponse(
            status_code=200,
            mimetype='text/plain',
            body=output.strip()
        )

    return jsonify([species.to_basic_dict() for species in speciess])


def get_ncbi_data(taxonomy_id):
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403
    Entrez.api_key = os.getenv('NIH_API_KEY')
    handle = Entrez.efetch(db='Taxonomy', id=str(taxonomy_id), retmode='xml')
    records = Entrez.read(handle)
    if len(records) < 1:
        return jsonify(
            {'detail': f'Species not found with taxonomy id "{taxonomy_id}"'},
            404
        )
    record = records[0]
    scientific_name = record.get('ScientificName', '')

    # confirm that the "OtherNames" key exists
    other_names = record.get('OtherNames')
    if other_names is not None:
        synonyms = other_names.get('Synonym', []) + other_names.get('GenbankSynonym', [])
    else:
        synonyms = []

    return jsonify({
        'scientificName': scientific_name,
        'synonyms': synonyms
    })


def requests_pending(api_key=None):
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403
    requests = db.session.query(TolidRequest) \
        .filter(TolidRequest.status == 'Pending') \
        .order_by(TolidRequest.request_id.asc()) \
        .all()
    return jsonify(requests)


def accept_tol_id_request(request_id=None):
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403

    request = db.session.query(TolidRequest) \
        .filter(TolidRequest.request_id == request_id) \
        .one_or_none()
    if request is None:
        return jsonify([])

    species = db.session.query(TolidSpecies) \
        .filter(TolidSpecies.taxonomy_id == request.species_id) \
        .one_or_none()

    if species is None:
        return jsonify({'detail': f'Species with taxonomyId {request.species_id}'
                        ' cannot be found'}), 400

    specimen = accept_request(request)
    return jsonify([specimen])


def reject_tol_id_request(request_id=None, reason=None):
    role = db.session.query(TolidRole) \
        .filter(TolidRole.role == 'admin') \
        .filter(TolidRole.user_id == connexion.context['user']) \
        .one_or_none()
    if role is None:
        return jsonify({'detail': 'User does not have permission to use this function'}), 403

    request = db.session.query(TolidRequest) \
        .filter(TolidRequest.request_id == request_id) \
        .one_or_none()
    if request is None:
        return jsonify([])

    reject_request(request, reason)
    return jsonify([request])
