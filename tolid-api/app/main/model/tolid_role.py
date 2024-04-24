# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidRole(Base):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)  # noqa
    name = db.Column(db.String(), nullable=False, unique=True)

    _role_bindings = db.relationship(
        'TolidRoleBinding',
        back_populates='role',
        lazy=False
    )

    def to_dict(self):
        return {'role': self.name}
