# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidUser(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)  # noqa
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    organisation = db.Column(db.String(), nullable=True)

    _role_bindings = db.relationship(
        'TolidRoleBinding',
        back_populates='user',
        lazy=False
    )

    def to_dict(self):
        return {'name': self.name,
                'email': self.email,
                'organisation': ('' if self.organisation is None else self.organisation),
                'roles': self.roles}

    @property
    def user_id(self) -> int:
        return self.id

    @property
    def role_names(self) -> list[str]:
        return [
            b.role.name for b in self._role_bindings
        ]
