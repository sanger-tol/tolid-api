# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy import func

from .base import Base, db
from .tolid_specimen import TolidSpecimen


class TolidSpecies(Base):
    __tablename__ = 'species'
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
    specimens = db.relationship('TolidSpecimen', back_populates='species',
                                lazy=False, order_by='TolidSpecimen.number')

    def to_basic_dict(self):
        return {'prefix': self.prefix,
                'scientificName': self.name,
                'taxonomyId': self.taxonomy_id,
                'commonName': self.common_name,
                'genus': self.genus,
                'family': self.family,
                'order': self.tax_order,
                'taxaClass': self.tax_class,
                'phylum': self.phylum,
                'kingdom': self.kingdom}

    def to_dict(self):
        basic = self.to_basic_dict()
        additional = {'currentHighestTolidNumber': self.current_highest_tolid_number()}
        return {**basic, **additional}  # Merge the two together

    def to_long_dict(self):
        short = self.to_dict()
        tolids = []
        for specimen in self.specimens:
            tolid = {'tolId': specimen.tolid,
                     'specimen': {'specimenId': specimen.specimen_id}}
            tolids.append(tolid)
        additional = {'tolIds': tolids}
        return {**short, **additional}  # Merge the two together

    def current_highest_tolid_number(self):
        # What is the current highest specimen number?
        highest = db.session.query(func.max(TolidSpecimen.number)) \
            .filter(TolidSpecimen.species_id == self.taxonomy_id) \
            .scalar()
        if not highest:
            highest = 0
        return highest
