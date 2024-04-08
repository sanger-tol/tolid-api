# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TolidRole(Base):
    __tablename__ = 'role'
    role_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user = relationship(
        'TolidUser',
        back_populates='roles',
        uselist=False,
        foreign_keys=[user_id]
    )

    def to_dict(self):
        return {'role': self.role}
