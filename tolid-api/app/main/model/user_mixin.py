# SPDX-FileCopyrightText: 2023 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from sqlalchemy.orm import (
    Mapped,
    declared_attr,
    mapped_column,
    relationship
)


class UserMixin:

    @declared_attr
    def name(self) -> Mapped[str]:
        return mapped_column()

    @declared_attr
    def workplace(self) -> Mapped[str]:
        return mapped_column()

    @declared_attr
    def requests(self) -> Mapped[list['Request']]:  # noqa F821
        return relationship(
            back_populates='user'
        )

    @declared_attr
    def specimens(self) -> Mapped[list['Specimen']]:  # noqa F821
        return relationship(
            back_populates='user'
        )
