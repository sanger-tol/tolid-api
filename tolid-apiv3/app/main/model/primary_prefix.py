# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PrimaryPrefix(Base):
    __tablename__ = 'primary_prefix'

    letter: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    secondary_prefixes: Mapped[List['SecondaryPrefix']] = relationship(back_populates='primary_prefix')  # noqa F821

    @classmethod
    def get_id_column_name(cls) -> str:
        return 'letter'
