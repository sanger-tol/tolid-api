# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SecondaryPrefix(Base):
    __tablename__ = 'secondary_prefix'

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa A003
    letter: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()

    primary_prefix_letter: Mapped[str] = mapped_column(ForeignKey('primary_prefix.letter'))
    primary_prefix: Mapped['PrimaryPrefix'] = relationship(back_populates='secondary_prefixes')  # noqa F821
