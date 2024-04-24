# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidToken(Base):
    __tablename__ = 'token'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)  # noqa

    token = db.Column(db.String(), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    expires_at = db.Column(
        db.DateTime(),
        nullable=False
    )
    oidc = db.Column(db.Boolean(), nullable=False, default=True)

    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False
    )
    user = db.relationship(
        'TolidUser',
        back_populates='_tokens',
        foreign_keys=[user_id]
    )
