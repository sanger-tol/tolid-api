from .base import Base, db
from .tolid_species import TolidSpecies

class TolidRequest(Base):
    __tablename__ = "request"
    request_id = db.Column(db.Integer, primary_key=True)
    specimen_id = db.Column(db.String())
    species_id = db.Column(db.Integer)
    status = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("TolidUser", uselist=False, foreign_keys=[created_by])

    db.UniqueConstraint('specimen_id', 'species_id', name='request_specimen_species_1')

    def to_dict(cls):
        species = db.session.query(TolidSpecies).filter(TolidSpecies.taxonomy_id == cls.species_id).one_or_none()
        if species is None:
            return {
                'id': cls.request_id,
                'status': cls.status,
                'species': {'taxonomyId': cls.species_id},
                'specimen': {'specimenId': cls.specimen_id}
                } 
        else:
            return {
                'id': cls.request_id,
                'status': cls.status,
                'species': species,
                'specimen': {'specimenId': cls.specimen_id}
                } 
