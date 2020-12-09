from .base import Base, db

class PnaSpecimen(Base):
    __tablename__ = "specimen"
    specimen_id = db.Column(db.String(), primary_key=True)

    species_id = db.Column(db.Integer, db.ForeignKey('species.taxonomy_id'))
    species = db.relationship("PnaSpecies", uselist=False, foreign_keys=[species_id])
    public_name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("PnaUser", uselist=False, foreign_keys=[created_by])

    def to_dict(cls):
        return {'tolId': cls.public_name,
            'species': cls.species,
            'specimen': {'specimenId': cls.specimen_id} # This will change when we change model
            } 
