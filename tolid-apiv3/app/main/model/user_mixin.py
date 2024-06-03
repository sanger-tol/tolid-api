# SPDX-FileCopyrightText: 2023 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy.orm import (
    Mapped,
    declared_attr,
    relationship
)


class UserMixin:

    @declared_attr
    def requests(self) -> Mapped[list['Request']]:  # noqa F821
        return relationship(
            back_populates='user'
        )

    @declared_attr
    def specimens(self) -> Mapped[list['Tolid']]:
        return relationship(
            back_populates='user'
        )
