# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from tol.sql import create_sql_datasource

from .. import model


models_list = [
    model.tolid_primary_prefix,
    model.tolid_request,
    model.tolid_role,
    model.tolid_secondary_prefix,
    model.tolid_species,
    model.tolid_specimen,
    model.tolid_user
]


tolid = create_sql_datasource(
    models_list,
    os.environ['DB_URI']
)
