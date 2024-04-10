# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidRoleBinding(Base):
    __tablename__ = 'role_binding'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.id'),
        primary_key=True
    )
    user = db.relationship(
        'TolidUser',
        back_populates='_role_bindings',
        foreign_keys=[user_id]
    )

    role_id = db.Column(
        db.Integer(),
        db.ForeignKey('role.id'),
        primary_key=True
    )
    role = db.relationship(
        'TolidRole',
        back_populates='_role_bindings',
        foreign_keys=[role_id]
    )
