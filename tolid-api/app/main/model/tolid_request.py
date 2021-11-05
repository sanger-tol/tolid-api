# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db
from .tolid_species import TolidSpecies


class TolidRequest(Base):
    __tablename__ = "request"
    request_id = db.Column(db.Integer, primary_key=True)
    specimen_id = db.Column(db.String())
    species_id = db.Column(db.Integer)
    status = db.Column(db.String())
    reason = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("TolidUser", uselist=False, foreign_keys=[created_by])
    confirmation_name = db.Column(db.String(), nullable=True)

    db.UniqueConstraint('specimen_id', 'species_id', name='request_specimen_species_1')

    def to_dict(cls):
        species = db.session.query(TolidSpecies) \
            .filter(TolidSpecies.taxonomy_id == cls.species_id) \
            .one_or_none()
        if species is None:
            dict_request = {
                'requestId': cls.request_id,
                'status': cls.status,
                'reason': cls.reason,
                'createdBy': cls.user,
                'species': {'taxonomyId': cls.species_id},
                'specimen': {'specimenId': cls.specimen_id},
                }
        else:
            dict_request = {
                'requestId': cls.request_id,
                'status': cls.status,
                'reason': cls.reason,
                'createdBy': cls.user,
                'species': species,
                'specimen': {'specimenId': cls.specimen_id},
                }
        if cls.confirmation_name is not None:
            dict_request['confirmationName'] = cls.confirmation_name
        return dict_request
