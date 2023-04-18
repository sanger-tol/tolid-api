# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from .base import Base, db


class TolidRole(Base):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('TolidUser', back_populates='roles',
                           uselist=False, foreign_keys=[user_id])

    def to_dict(self):
        return {'role': self.role}
