# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidSpecimen(Base):
    __tablename__ = 'specimen'
    specimen_id = db.Column(db.String())

    species_id = db.Column(db.Integer, db.ForeignKey('species.taxonomy_id'))
    species = db.relationship('TolidSpecies', back_populates='specimens',
                              uselist=False, foreign_keys=[species_id])
    tolid = db.Column(db.String(), primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('TolidUser', uselist=False, foreign_keys=[created_by])

    def to_dict(self):
        return {'tolId': self.tolid,
                'species': self.species,
                'specimen': {'specimenId': self.specimen_id},
                'user': self.user}
