from .base import Base, db

class PnaSpecimen(Base):
    __tablename__ = "specimen"
    specimen_id = db.Column(db.String(), primary_key=True)

    species_id = db.Column(db.Integer, db.ForeignKey('species.taxonomy_id'))
    species = db.relationship("PnaSpecies", uselist=False, foreign_keys=[species_id])
    number = db.Column(db.Integer, nullable=False)

    def to_dict(cls):
        print("JSONIFYING")
        return {'prefix': cls.species.prefix, 
            'publicName': cls.species.prefix + str(cls.number),
            'species': cls.species.name, 
            'taxonomyId': cls.species.taxonomy_id, 
            'commonName': cls.species.common_name, 
            'genus': cls.species.genus, 
            'family': cls.species.family, 
            'order': cls.species.tax_order, 
            'taxaClass': cls.species.tax_class, 
            'phylum': cls.species.phylum,
            'specimenId': cls.specimen_id}
