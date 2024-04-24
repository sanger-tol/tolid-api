# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Request(Base):
    __tablename__ = 'request'

    request_id: Mapped[str] = mapped_column(primary_key=True)
    specimen_id: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    reason: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column()
    confirmation_name: Mapped[str] = mapped_column()

    species_id: Mapped[int] = mapped_column(ForeignKey('species.taxonomy_id'))
    species: Mapped['Species'] = relationship(back_populates='requests')  # noqa F821

    created_by: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='requests')  # noqa F821

    @classmethod
    def get_id_column_name(cls) -> str:
        return 'request_id'
