from flask import jsonify, send_from_directory
from sqlalchemy import or_
from swagger_server.db_utils import create_new_specimen
from swagger_server.model import db, TolidSpecies, TolidSpecimen, \
    TolidUser, TolidRole
from swagger_server.excel_utils import validate_excel
import connexion
import tempfile


def add_specimen(taxonomy_id=None, specimen_id=None, api_key=None):
    """adds a specimen and assigns a ToLID

    Adds a new ToLID to the system

    :param taxonomy_id: valid NCBI Taxonomy identifier
    :type taxonomy_id: str
    :param specimen_id: valid GAL specimen identifier
    :type specimen_id: str

    :return: JSON with complete ToLID and taxa structure
    """
    user = db.session.query(TolidUser) \
        .filter(TolidUser.user_id == connexion.context["user"]) \
        .one_or_none()
    species = db.session.query(TolidSpecies) \
        .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
        .one_or_none()

    if species is None:
        return "Species with taxonomyId " + str(taxonomy_id) \
            + " cannot be found", 400

    role = db.session.query(TolidRole) \
        .filter(or_(TolidRole.role == 'creator', TolidRole.role == 'admin')) \
        .filter(TolidRole.user_id == connexion.context["user"]) \
        .one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403

    specimen = db.session.query(TolidSpecimen) \
        .filter(TolidSpecimen.specimen_id == specimen_id) \
        .filter(TolidSpecimen.species_id == taxonomy_id) \
        .one_or_none()

    if specimen is None:
        specimen = create_new_specimen(species, specimen_id, user)
        db.session.add(specimen)
        db.session.commit()

    return jsonify([specimen])


def bulk_search_specimens(body=None, api_key=None):
    role = db.session.query(TolidRole) \
        .filter(or_(TolidRole.role == 'creator', TolidRole.role == 'admin')) \
        .filter(TolidRole.user_id == connexion.context["user"]) \
        .one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403

    user = db.session.query(TolidUser) \
        .filter(TolidUser.user_id == connexion.context["user"]) \
        .one_or_none()
    specimens = []
    # body contains the rows of data
    if body:
        for row in body:
            specimen_id = row['specimenId']
            taxonomy_id = row['taxonomyId']
            species = db.session.query(TolidSpecies) \
                .filter(TolidSpecies.taxonomy_id == taxonomy_id) \
                .one_or_none()

            if species is None:
                db.session.rollback()
                return "Species with taxonomyId " + str(taxonomy_id) \
                    + " cannot be found", 400

            specimen = db.session.query(TolidSpecimen) \
                .filter(TolidSpecimen.species_id == taxonomy_id) \
                .filter(TolidSpecimen.specimen_id == specimen_id) \
                .one_or_none()

            if specimen is None:
                specimen = create_new_specimen(species, specimen_id, user)

            specimens.append(specimen)
            db.session.add(specimen)
        db.session.commit()

    return jsonify(specimens)


def validate_manifest(excel_file=None, species_column_heading="scientific_name"):  # noqa: E501
    role = db.session.query(TolidRole) \
        .filter(or_(TolidRole.role == 'creator', TolidRole.role == 'admin')) \
        .filter(TolidRole.user_id == connexion.context["user"]) \
        .one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403

    user = db.session.query(TolidUser) \
        .filter(TolidUser.user_id == connexion.context["user"]) \
        .one_or_none()
    uploaded_file = connexion.request.files['excelFile']

    # Save to a temporary location
    dir = tempfile.TemporaryDirectory()
    uploaded_file.save(dir.name+'/manifest.xlsx')

    # Do the validation
    (validated, updated_filename, errors) = \
        validate_excel(dirname=dir.name,
                       filename='manifest.xlsx',
                       user=user,
                       species_column_heading=species_column_heading)
    if validated:
        # Stream out the validated Excel file and remove
        return send_from_directory(dir.name, filename=updated_filename,
                                   as_attachment=True)
    else:
        # Return the error
        return jsonify({"errors": errors}), 400

    # Remove old file
    dir.cleanup()
