# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TolidSecondaryPrefix(Base):
    __tablename__ = 'secondary_prefix'

    letter: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    primary_prefix_letter: Mapped[str] = mapped_column(
        ForeignKey('primary_prefix.letter'),
        primary_key=True
    )
    primary_prefix = relationship(
        'TolidPrimaryPrefix',
        back_populates='secondary_prefixes',
        foreign_keys=[primary_prefix_letter]
    )

    def to_dict(self):
        return {'letter': self.letter,
                'name': self.name}
