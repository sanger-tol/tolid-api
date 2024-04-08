# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os
from typing import Any

from Bio import Entrez

from flask import jsonify

from main.controllers.auth import require_admin
import main.controllers.datasource as ds
from main.db_utils import accept_request, reject_request
from main.model import TolidRequest, TolidSpecies, TolidSpecimen, \
    session_factory




@require_admin
def add_species(body: dict[str, Any] = None):

    with session_factory() as session:

        species = session.query(TolidSpecies) \
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

        session.add(species)
        session.commit()

        return jsonify([species.to_long_dict()])


@require_admin
def edit_species(taxonomy_id=None, body=None):
    if not taxonomy_id.isnumeric():
        return 'taxonomyId should be numeric', 404

    with session_factory() as session:

        species = session.query(TolidSpecies) \
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

        session.commit()

        return jsonify([species.to_long_dict()])


@require_admin
def list_specimens(taxonomy_id=None, skip=None, limit=None):

    with session_factory() as session:
        if taxonomy_id is None:
            specimens = session.query(TolidSpecimen) \
                .order_by(TolidSpecimen.species_id) \
                .order_by(TolidSpecimen.specimen_id) \
                .order_by(TolidSpecimen.number) \
                .all()
        else:
            species = session.query(TolidSpecies) \
                .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
                .one_or_none()

            if species is None:
                return jsonify({'detail': 'Species with taxonomyId ' + str(taxonomy_id)
                            + ' cannot be found'}), 400

            specimens = session.query(TolidSpecimen) \
                .filter(TolidSpecimen.species_id == taxonomy_id) \
                .order_by(TolidSpecimen.specimen_id) \
                .order_by(TolidSpecimen.number) \
                .all()

    output = ''
    for specimen in specimens:
        output += specimen.tolid + '\t' + specimen.species.name + '\t' \
            + specimen.specimen_id + '\t' + str(specimen.number) + '\n'
    return output.strip()


def list_species_plaintext(speciess: list[TolidSpecies]) -> str:
    output = ''
    for species in speciess:
        output += species.prefix + '\t' + species.name + '\t' + str(species.taxonomy_id) \
            + '\t' + species.common_name + '\t' + species.genus + '\t' + species.family \
            + '\t' + species.tax_order + '\t' + species.tax_class + '\t' + species.phylum \
            + '\n'
    return output.strip()


@require_admin
def list_species(headers: dict[str, str]):
    with session_factory() as session:

        speciess = session.query(TolidSpecies).order_by(TolidSpecies.taxonomy_id).all()

        accept_header = str(headers.get('accept', ''))

        if accept_header.startswith('text/plain'):
            # Set Content-Type header
            list_species_plaintext(speciess), 200, {'Content-Type': 'text/plain'}

        return jsonify([species.to_basic_dict() for species in speciess])


@require_admin
def get_ncbi_data(taxonomy_id):
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


@require_admin
def requests_pending():
    with session_factory() as session:
        requests = session.query(TolidRequest) \
            .filter(TolidRequest.status == 'Pending') \
            .order_by(TolidRequest.request_id.asc()) \
            .all()
        return jsonify(requests)


@require_admin
def accept_tol_id_request(request_id=None):

    with session_factory() as session:
        request = session.query(TolidRequest) \
            .filter(TolidRequest.request_id == request_id) \
            .one_or_none()
        if request is None:
            return jsonify([])

        species = session.query(TolidSpecies) \
            .filter(TolidSpecies.taxonomy_id == request.species_id) \
            .one_or_none()

        if species is None:
            return jsonify({'detail': f'Species with taxonomyId {request.species_id}'
                            ' cannot be found'}), 400

        specimen = accept_request(request, session)

        return jsonify([specimen])


@require_admin
def reject_tol_id_request(request_id=None, reason=None):

    with session_factory() as sess:
        request = sess.query(TolidRequest) \
            .filter(TolidRequest.request_id == request_id) \
            .one_or_none()
        if request is None:
            return jsonify([])

        reject_request(request, reason, sess)

        return jsonify([request])
