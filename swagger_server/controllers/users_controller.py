from swagger_server.model import db, TolidSpecies, TolidSpecimen, TolidUser, TolidRole, TolidRequest
from flask import jsonify
from swagger_server.db_utils import create_new_specimen
from sqlalchemy import or_
import connexion

def search_specimen(specimen_id=None, skip=None, limit=None):  
    """searches DToL ToLIDs

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :param taxonomyId: pass an optional search string for looking up a ToLID
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Specimen]
    """
    specimens = db.session.query(TolidSpecimen).filter(TolidSpecimen.specimen_id == specimen_id).all()

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
    """searches DToL ToLIDs

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :param taxonomyId: pass an optional search string for looking up a ToLID
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Specimen]
    """
    specimen = db.session.query(TolidSpecimen).filter(TolidSpecimen.public_name == tol_id).one_or_none()

    if specimen is None:
        return jsonify([])

    return jsonify([specimen])

def search_tol_id_by_taxon_specimen(taxonomy_id=None, specimen_id=None, skip=None, limit=None):  
    """searches DToL ToLIDs

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :param taxonomyId: pass an optional search string for looking up a ToLID
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Specimen]
    """
    specimen = db.session.query(TolidSpecimen).filter(TolidSpecimen.species_id == taxonomy_id).filter(TolidSpecimen.specimen_id == specimen_id).one_or_none()

    if specimen is None:
        return jsonify([])

    return jsonify([specimen])

def tol_ids_for_user(api_key=None):  
    """searches DToL ToLIDs for the current user

    By passing in the appropriate taxonomy string, you can search for available ToLIDs in the system 

    :rtype: List[Specimen]
    """
    user = db.session.query(TolidUser).filter(TolidUser.user_id == connexion.context["user"]).one_or_none()
    specimens = db.session.query(TolidSpecimen).filter(TolidSpecimen.created_by == connexion.context["user"]).order_by(TolidSpecimen.created_at.desc()).all()
    return jsonify(specimens)

def search_species(taxonomy_id=None, skip=None, limit=None):  
    """searches species

    By passing in the appropriate taxonomy string, you can search for available species in the system 

    :param taxonomyId: pass an optional taxonomy ID to filter by
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[Species]
    """

    species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == taxonomy_id).one_or_none()

    if species is None:
        return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

    return jsonify([species])

def requests_for_user(api_key=None):  
    """searches DToL ToLID requests for the current user

    By passing in the appropriate taxonomy string, you can search for ToLID requests in the system 

    :rtype: List[Specimen]
    """
    user = db.session.query(TolidUser).filter(TolidUser.user_id == connexion.context["user"]).one_or_none()
    requests = db.session.query(TolidRequest).filter(TolidRequest.created_by == connexion.context["user"]).order_by(TolidRequest.created_at.desc()).all()
    return jsonify(requests)

def bulk_add_requests(body=None, api_key=None):  
    user = db.session.query(TolidUser).filter(TolidUser.user_id == connexion.context["user"]).one_or_none()
    requests = []
    # body contains the rows of data
    if body:
        for row in body:
            specimen_id = row['specimenId']
            taxonomy_id = row['taxonomyId']
            specimen = db.session.query(TolidSpecimen).filter(TolidSpecimen.species_id == taxonomy_id).filter(TolidSpecimen.specimen_id == specimen_id).one_or_none()
            if specimen is not None:
                db.session.rollback()
                return "A ToLID already exists for specimenId "+specimen_id+" and taxonomyId "+str(taxonomy_id), 400

            request = db.session.query(TolidRequest).filter(TolidRequest.specimen_id == specimen_id).filter(TolidRequest.species_id == taxonomy_id).one_or_none()
            if request is None:
                request = TolidRequest(specimen_id=specimen_id, species_id=taxonomy_id, status="Pending")
                request.user = user
            else:
                if request.user != user:
                    db.session.rollback()
                    return "Another user has requested a ToLID for specimenId "+specimen_id+" and taxonomyId "+str(taxonomyId), 400

            requests.append(request)
            db.session.add(request)
        db.session.commit()

    return jsonify(requests)

def search_request(request_id=None, skip=None, limit=None):  
    request = db.session.query(TolidRequest).filter(TolidRequest.request_id == request_id).one_or_none()

    if request is None:
        return jsonify([])

    return jsonify([request])
