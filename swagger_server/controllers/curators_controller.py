# from swagger_server.models.public_name import PublicName 
# from swagger_server import util
from flask import jsonify, send_from_directory
from swagger_server.db_utils import create_new_specimen
from swagger_server.model import db, PnaSpecies, PnaSpecimen, PnaUser
from swagger_server.excel_utils import validate_excel
import connexion
import tempfile


def add_public_name(taxonomy_id=None, specimen_id=None, api_key=None): 
    """adds a public name

    Adds a new public name to the system 

    :param taxonomy_id: valid NCBI Taxonomy identifier
    :type taxonomy_id: str
    :param specimen_id: valid GAL specimen identifier
    :type specimen_id: str

    :return: JSON with complete public name and taxa structure
    """
    user = db.session.query(PnaUser).filter(PnaUser.api_key == api_key).one_or_none()
    species = db.session.query(PnaSpecies).filter(PnaSpecies.taxonomy_id == taxonomy_id).one_or_none()

    if species is None:
        return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

    specimen = db.session.query(PnaSpecimen).filter(PnaSpecimen.specimen_id == specimen_id).one_or_none()

    if specimen is not None:
        if specimen.species.taxonomy_id != species.taxonomy_id:
            return "Species of specimen "+str(specimen_id)+" is "+ specimen.species.name + " but was expecting "+species.name, 400
    else:
        specimen = create_new_specimen(species, specimen_id, user)
        db.session.add(specimen)
        db.session.commit()

    return jsonify([specimen])

def validate_manifest(excel_file=None, species_column_heading="scientific_name"):  # noqa: E501
    """Validate an excel manifest

    Validates an excel manifest and offers option to download manifest with public names filled in  # noqa: E501

    :param type: 
    :type type: str
    :param file_name: 
    :type file_name: strstr

    :rtype: None
    """
    user = db.session.query(PnaUser).filter(PnaUser.user_id == connexion.context["user"]).one_or_none()
    uploaded_file = connexion.request.files['excelFile']

    # Save to a temporary location
    dir = tempfile.TemporaryDirectory()
    uploaded_file.save(dir.name+'/manifest.xlsx')

    # Do the validation
    (validated, updated_filename, errors) = validate_excel(dirname=dir.name, filename='manifest.xlsx', user=user, species_column_heading=species_column_heading)
    if validated:
        # Stream out the validated Excel file and remove
        return send_from_directory(dir.name, filename=updated_filename, as_attachment=True)
    else:
        # Return the error
        return jsonify({"errors": errors}), 400

    # Remove old file
    dir.cleanup()