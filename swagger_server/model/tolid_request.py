from .base import Base, db
from .tolid_species import TolidSpecies

class TolidRequest(Base):
    __tablename__ = "request"
    specimen_id = db.Column(db.String(), primary_key=True)

    species_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("TolidUser", uselist=False, foreign_keys=[created_by])

    def to_dict(cls):
        species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == cls.species_id).one_or_none()
        if species is None:
            return {
                'species': {'taxonomyId': cls.species_id},
                'specimen': {'specimenId': cls.specimen_id} # This will change when we change model
                } 
        else:
            return {
                'species': species,
                'specimen': {'specimenId': cls.specimen_id} # This will change when we change model
                } 
