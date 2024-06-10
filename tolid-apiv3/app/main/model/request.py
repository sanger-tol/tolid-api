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

    # We don't make this a relationship because we may have species_ids that
    # don't exist in the species table
    species_id: Mapped[int] = mapped_column()

    created_by: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='requests')  # noqa F821

    @classmethod
    def get_id_column_name(cls) -> str:
        return 'request_id'
