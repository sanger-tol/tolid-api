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
    