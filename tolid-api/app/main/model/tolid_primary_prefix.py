# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidPrimaryPrefix(Base):
    __tablename__ = 'primary_prefix'
    letter = db.Column(db.String, primary_key=True)
    name = db.Column(db.String())
    secondary_prefixes = db.relationship('TolidSecondaryPrefix', back_populates='primary_prefix',
                                         lazy=False, order_by='TolidPrimaryPrefix.letter')

    def to_dict(self):
        return {'letter': self.letter,
                'name': self.name,
                'secondaryPrefixes': self.secondary_prefixes}
