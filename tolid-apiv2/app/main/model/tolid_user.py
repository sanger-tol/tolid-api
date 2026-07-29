# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidUser(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)  # noqa
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    workplace = db.Column(db.String(), nullable=True)

    _role_bindings = db.relationship(
        'TolidRoleBinding',
        back_populates='user',
        lazy=False
    )
    _tokens = db.relationship(
        'TolidToken',
        back_populates='user',
        lazy=False
    )

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'workplace': ('' if self.workplace is None else self.workplace),
            'roles': [
                {'role': r} for r in self.role_names
            ]
        }

    @property
    def user_id(self) -> int:
        return self.id

    @property
    def role_names(self) -> list[str]:
        return [
            b.role.name for b in self._role_bindings
        ]
