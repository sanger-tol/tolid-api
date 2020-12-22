from sqlalchemy import func
from swagger_server.model import db, TolidSpecies, TolidSpecimen

def create_new_specimen(species, specimen_id, user):
    # What is the current highest specimen number?
    highest = db.session.query(func.max(TolidSpecimen.number)).filter(TolidSpecimen.species_id == species.taxonomy_id).scalar()
    if not highest:
        highest = 0
    number = highest + 1
    specimen = TolidSpecimen(specimen_id=specimen_id, number=number, public_name=species.prefix+str(number))
    specimen.species = species
    specimen.user = user
    return specimen

def accept_request(request):
    species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == request.species_id).one_or_none()
    if species is None:
        raise Exception("Species not in database")
    specimen = create_new_specimen(species, request.specimen_id, request.user)
    db.session.add(specimen)
    db.session.delete(request)
    db.session.commit()
    return specimen

def reject_request(request):
    request.status = "Rejected"
    db.session.commit()
    return request