# SPDX-FileCopyrightText: 2022 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from marshmallow_jsonapi.fields import Str

from tol.api_base.schema import BaseSchema, setup_schema

from ..model import Species


@setup_schema
class SpeciesSchema(BaseSchema):
    class Meta(BaseSchema.BaseMeta):
        model = Species

    id = Str(attribute='taxonomy_id', dump_only=True)  # noqa A003
