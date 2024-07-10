# SPDX-FileCopyrightText: 2023 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Species(Base):
    __tablename__ = 'species'

    taxonomy_id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    common_name: Mapped[str] = mapped_column()
    genus: Mapped[str] = mapped_column()
    family: Mapped[str] = mapped_column()
    tax_order: Mapped[str] = mapped_column()
    tax_class: Mapped[str] = mapped_column()
    phylum: Mapped[str] = mapped_column()
    kingdom: Mapped[str] = mapped_column()

    specimens: Mapped[List['Specimen']] = relationship(back_populates='species')  # noqa F821

    @classmethod
    def get_id_column_name(cls) -> str:
        return 'taxonomy_id'
