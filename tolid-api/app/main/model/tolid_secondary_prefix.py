# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidSecondaryPrefix(Base):
    __tablename__ = 'secondary_prefix'
    letter = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    primary_prefix_letter = db.Column(db.String(), db.ForeignKey('primary_prefix.letter'),
                                      primary_key=True)
    primary_prefix = db.relationship('TolidPrimaryPrefix', back_populates='secondary_prefixes',
                                     foreign_keys=[primary_prefix_letter])

    def to_dict(self):
        return {'letter': self.letter,
                'name': self.name}
