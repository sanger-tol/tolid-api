# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import typing
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from .tolid_species import TolidSpecies


class TolidSpecimen(Base):
    __tablename__ = 'specimen'
    specimen_id: Mapped[str] = mapped_column()

    species_id: Mapped[int] = mapped_column(ForeignKey('species.taxonomy_id'))
    species: Mapped['TolidSpecies'] = relationship(
        'TolidSpecies',
        back_populates='specimens',
        uselist=False,
        foreign_keys=[species_id]
    )
    tolid: Mapped[str] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    created_by: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user = relationship('TolidUser', uselist=False, foreign_keys=[created_by])

    def to_dict(self):
        return {'tolId': self.tolid,
                'species': self.species,
                'specimen': {'specimenId': self.specimen_id},
                'user': self.user}
