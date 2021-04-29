from .base import Base, db
from sqlalchemy import func
from .tolid_specimen import TolidSpecimen


class TolidSpecies(Base):
    __tablename__ = "species"
    taxonomy_id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String())
    name = db.Column(db.String())
    common_name = db.Column(db.String())
    genus = db.Column(db.String())
    family = db.Column(db.String())
    tax_order = db.Column(db.String())
    tax_class = db.Column(db.String())
    phylum = db.Column(db.String())
    kingdom = db.Column(db.String())
    specimens = db.relationship('TolidSpecimen', back_populates="species",
                                lazy=False, order_by='TolidSpecimen.number')

    def to_dict(cls):
        return {'prefix': cls.prefix,
                'scientificName': cls.name,
                'taxonomyId': cls.taxonomy_id,
                'commonName': cls.common_name,
                'genus': cls.genus,
                'family': cls.family,
                'order': cls.tax_order,
                'taxaClass': cls.tax_class,
                'phylum': cls.phylum,
                'kingdom': cls.kingdom,
                'currentHighestTolidNumber': cls.current_highest_tolid_number()}

    def to_long_dict(cls):
        short = cls.to_dict()
        tolIds = []
        for specimen in cls.specimens:
            tolId = {'tolId': specimen.public_name,
                     'specimen': {'specimenId': specimen.specimen_id}}
            tolIds.append(tolId)
        additional = {'tolIds': tolIds}
        return {**short, **additional}  # Merge the two together

    def current_highest_tolid_number(cls):
        # What is the current highest specimen number?
        highest = db.session.query(func.max(TolidSpecimen.number)) \
            .filter(TolidSpecimen.species_id == cls.taxonomy_id) \
            .scalar()
        if not highest:
            highest = 0
        return highest
