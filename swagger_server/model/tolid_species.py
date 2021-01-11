from .base import Base, db


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
    specimens = db.relationship('TolidSpecimen', lazy=False)

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
                'kingdom': cls.kingdom}
