# SPDX-FileCopyrightText: 2023 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Tolid(Base):
    __tablename__ = 'specimen'

    tolid: Mapped[str] = mapped_column(primary_key=True)
    specimen_id: Mapped[str] = mapped_column()
    number: Mapped[int] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column()
    legacy_name: Mapped[str] = mapped_column()

    species_id: Mapped[int] = mapped_column(ForeignKey('species.taxonomy_id'))
    species: Mapped['TolidSpecies'] = relationship(back_populates='tolids')  # noqa F821

    @classmethod
    def get_id_column_name(cls) -> str:
        return 'tolid'
