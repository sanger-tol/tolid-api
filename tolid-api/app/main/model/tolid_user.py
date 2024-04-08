# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TolidUser(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    organisation: Mapped[str] = mapped_column(nullable=True)
    api_key: Mapped[str] = mapped_column(nullable=True, unique=True)
    token: Mapped[str] = mapped_column(nullable=True, unique=True)
    roles = relationship('TolidRole', lazy=False, back_populates='user')

    def to_dict(self):
        return {'name': self.name,
                'email': self.email,
                'organisation': ('' if self.organisation is None else self.organisation),
                'roles': self.roles}
