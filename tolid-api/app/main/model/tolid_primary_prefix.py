# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from .tolid_secondary_prefix import TolidSecondaryPrefix


class TolidPrimaryPrefix(Base):
    __tablename__ = 'primary_prefix'

    letter: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    secondary_prefixes: Mapped[list['TolidSecondaryPrefix']] = relationship(
        'TolidSecondaryPrefix',
        back_populates='primary_prefix',
        lazy=False,
        order_by='TolidPrimaryPrefix.letter'
    )

    def to_dict(self):
        return {'letter': self.letter,
                'name': self.name,
                'secondaryPrefixes': self.secondary_prefixes}
