# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SecondaryPrefix(Base):
    __tablename__ = 'secondary_prefix'

    letter: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    primary_prefix_letter: Mapped[str] = mapped_column(ForeignKey('primary_prefix.letter'))
    primary_prefix: Mapped['PrimaryPrefix'] = relationship(back_populates='secondary_prefixes')  # noqa F821

    @classmethod
    def get_id_column_name(cls) -> str:
        return 'letter'
