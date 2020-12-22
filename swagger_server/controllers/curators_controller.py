from flask import jsonify, send_from_directory
from swagger_server.db_utils import create_new_specimen
from swagger_server.model import db, TolidSpecies, TolidSpecimen, TolidUser, TolidRole, TolidRequest
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
    user = db.session.query(TolidUser).filter(TolidUser.user_id == connexion.context["user"]).one_or_none()
    species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == taxonomy_id).one_or_none()

    if species is None:
        return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

    specimen = db.session.query(TolidSpecimen).filter(TolidSpecimen.specimen_id == specimen_id).filter(TolidSpecimen.species_id == taxonomy_id).one_or_none()

    if specimen is None:
        specimen = create_new_specimen(species, specimen_id, user)
        db.session.add(specimen)
        db.session.commit()

    return jsonify([specimen])

def add_species(body=None, api_key=None): 
    """adds a species

    Adds a new species to the system 

    :return: JSON with complete ToLID and taxa structure
    """
    role = db.session.query(TolidRole).filter(TolidRole.role == 'admin').filter(TolidRole.user_id == connexion.context["user"]).one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403

    species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == body["taxonomyId"]).one_or_none()
    if species is not None:
        return "Species with taxonomyId "+str(body["taxonomyId"])+" already exists", 400

    species = TolidSpecies()
    species.prefix=body["prefix"]
    species.name=body["scientificName"]
    species.taxonomy_id=body["taxonomyId"]
    species.common_name=body["commonName"]
    species.genus=body["genus"]
    species.family=body["family"]
    species.prefix=body["prefix"]
    species.tax_order=body["order"]
    species.tax_class=body["taxaClass"]
    species.phylum=body["phylum"]
    species.kingdom=body["kingdom"]

    db.session.add(species)
    db.session.commit()

    return jsonify([species])

def edit_species(taxonomy_id=None, body=None, api_key=None): 
    """modifies a species

    Modifies a species in the system 

    :return: JSON with complete ToLID and taxa structure
    """
    role = db.session.query(TolidRole).filter(TolidRole.role == 'admin').filter(TolidRole.user_id == connexion.context["user"]).one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403

    species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == taxonomy_id).one_or_none()
    if species is None:
        return "Species with taxonomyId "+str(taxonomy_id)+" does not exist", 400

    species.prefix=body["prefix"]
    species.name=body["scientificName"]
    # Don't allow the taxonomy ID to be changed
    # species.taxonomy_id=body["taxonomyId"]
    species.common_name=body["commonName"]
    species.genus=body["genus"]
    species.family=body["family"]
    species.prefix=body["prefix"]
    species.tax_order=body["order"]
    species.tax_class=body["taxaClass"]
    species.phylum=body["phylum"]
    species.kingdom=body["kingdom"]

    #db.session.add(species)
    db.session.commit()

    return jsonify([species])


def validate_manifest(excel_file=None, species_column_heading="scientific_name"):  # noqa: E501
    """Validate an excel manifest

    Validates an excel manifest and offers option to download manifest with ToLIDs filled in  # noqa: E501

    :param type: 
    :type type: str
    :param file_name: 
    :type file_name: strstr

    :rtype: None
    """
    user = db.session.query(TolidUser).filter(TolidUser.user_id == connexion.context["user"]).one_or_none()
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

def list_specimens(taxonomy_id=None, skip=None, limit=None):  
    """lists all ToLIDs

    By passing in the appropriate taxonomy string, you can limit the search to a particular species

    :param taxonomyId: pass an optional search string for looking up a ToLID
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Specimen]
    """
    role = db.session.query(TolidRole).filter(TolidRole.role == 'admin').filter(TolidRole.user_id == connexion.context["user"]).one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403

    if taxonomy_id is None:
        specimens = db.session.query(TolidSpecimen).order_by(TolidSpecimen.species_id).order_by(TolidSpecimen.specimen_id).order_by(TolidSpecimen.number).all()
    else:
        species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == taxonomy_id).one_or_none()

        if species is None:
            return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

        specimens = db.session.query(TolidSpecimen).filter(TolidSpecimen.species_id == taxonomy_id).order_by(TolidSpecimen.specimen_id).order_by(TolidSpecimen.number).all()

    output = ""
    for specimen in specimens:
        output += specimen.public_name+'\t'+specimen.species.name+'\t'+specimen.specimen_id+'\t'+str(specimen.number)+'\n'
    return output.strip()

def list_species():  
    """lists all species

    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Species]
    """
    role = db.session.query(TolidRole).filter(TolidRole.role == 'admin').filter(TolidRole.user_id == connexion.context["user"]).one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403

    speciess = db.session.query(TolidSpecies).order_by(TolidSpecies.taxonomy_id).all()

    output = ""
    for species in speciess:
        output += species.prefix+'\t'+species.name+'\t'+str(species.taxonomy_id)+'\t'+species.common_name+'\t'+species.genus+'\t'+species.family+'\t'+species.tax_order+'\t'+species.tax_class+'\t'+species.phylum+'\n'
    return output.strip()

def requests_pending(api_key=None):  
    role = db.session.query(TolidRole).filter(TolidRole.role == 'admin').filter(TolidRole.user_id == connexion.context["user"]).one_or_none()
    if role is None:
        return "User does not have permission to use this function", 403
    requests = db.session.query(TolidRequest).filter(TolidRequest.status == "Pending").order_by(TolidRequest.created_at.desc()).all()
    return jsonify(requests)
