# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from .base import Base
from .tolid_species import TolidSpecies


class TolidRequest(Base):
    __tablename__ = 'request'

    request_id: Mapped[int] = mapped_column(primary_key=True)
    specimen_id: Mapped[str] = mapped_column()
    species_id: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()
    reason: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now)
    created_by: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user = relationship('TolidUser', uselist=False, foreign_keys=[created_by])
    confirmation_name: Mapped[str] = mapped_column(nullable=True)

    UniqueConstraint('specimen_id', 'species_id', name='request_specimen_species_1')


    def to_dict(self, session: Session):
        species = session.query(TolidSpecies) \
            .filter(TolidSpecies.taxonomy_id == self.species_id) \
            .one_or_none()
        if species is None:
            dict_request = {
                'requestId': self.request_id,
                'status': self.status,
                'reason': self.reason,
                'createdBy': self.user,
                'species': {'taxonomyId': self.species_id},
                'specimen': {'specimenId': self.specimen_id},
            }
        else:
            dict_request = {
                'requestId': self.request_id,
                'status': self.status,
                'reason': self.reason,
                'createdBy': self.user,
                'species': species,
                'specimen': {'specimenId': self.specimen_id},
            }
        if self.confirmation_name is not None:
            dict_request['confirmationName'] = self.confirmation_name
        return dict_request
