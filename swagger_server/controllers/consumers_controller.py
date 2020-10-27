from swagger_server.model import db, PnaSpecies, PnaSpecimen  
from flask import jsonify
from swagger_server.db_utils import create_new_specimen

def search_public_name(taxonomy_id=None, specimen_id=None, skip=None, limit=None):  
    """searches DToL public names

    By passing in the appropriate taxonomy string, you can search for available public names in the system 

    :param taxonomyId: pass an optional search string for looking up a public name
    :type taxonomyId: str
    # :param skip: number of records to skip for pagination
    # :type skip: int
    # :param limit: maximum number of records to return
    # :type limit: int

    :rtype: List[PublicName]
    """

    species = db.session.query(PnaSpecies).filter(PnaSpecies.taxonomy_id == taxonomy_id).first()

    if not species:
        print("NO SPECIES FOUND")
        return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

    specimen = db.session.query(PnaSpecimen).filter(PnaSpecimen.specimen_id == specimen_id).first()

    if not specimen:
        print("NO SPECIMEN FOUND")
        return jsonify([])

    if specimen.species.taxonomy_id != species.taxonomy_id:
        return "Species of specimen "+str(specimen_id)+" is "+ specimen.species.name + " but was expecting "+species.name, 400

    return jsonify([specimen])

def bulk_search_public_name(body=None):  
    """searches DToL public names in bulk

    By passing in the appropriate taxonomy string, you can search for available public names in the system 

    :param bosy: 
    :type taxonomyId: str

    :rtype: List[PublicName]
    """

    specimens = []
    # body contains the rows of data
    if body:
        for row in body:
            specimen_id = row['specimenId']
            taxonomy_id = row['taxonomyId']
            species = db.session.query(PnaSpecies).filter(PnaSpecies.taxonomy_id == taxonomy_id).first()

            if not species:
                return "Species with taxonomyId "+str(taxonomy_id)+" cannot be found", 400

            specimen = db.session.query(PnaSpecimen).filter(PnaSpecimen.specimen_id == specimen_id).first()

            if specimen:
                if specimen.species.taxonomy_id != species.taxonomy_id:
                    return "Species of specimen "+str(specimen_id)+" is "+ specimen.species.name + " but was expecting "+species.name, 400
            else:
                specimen = create_new_specimen(species, specimen_id)

            specimens.append(specimen)

        for specimen in specimens:
            db.session.add(specimen)
        db.session.commit()

    return jsonify(specimens)
