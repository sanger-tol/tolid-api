# SPDX-FileCopyrightText: 2023 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from marshmallow_jsonapi.fields import Str

from tol.api_base.schema import BaseSchema, setup_schema

from ..model import Specimen


@setup_schema
class SpecimenSchema(BaseSchema):
    class Meta(BaseSchema.BaseMeta):
        model = Specimen

    id = Str(attribute='tolid', dump_only=True)  # noqa A003
