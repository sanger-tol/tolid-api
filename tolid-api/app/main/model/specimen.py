# SPDX-FileCopyrightText: 2023 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from tol.api_base.model import Base, db, setup_model


@setup_model
class Specimen(Base):
    __tablename__ = 'specimen'

    class Meta:
        type_ = 'specimens'
        id_column = 'tolid'

    tolid = db.Column(db.String(), primary_key=True)
    specimen_id = db.Column(db.String())

    species_id = db.Column(db.Integer, db.ForeignKey('species.taxonomy_id'))
    species = db.relationship('Species', back_populates='specimen',
                              uselist=False, foreign_keys=[species_id])
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    # created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # user = db.relationship('User', uselist=False, foreign_keys=[created_by])
