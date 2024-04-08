# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from tol.sql import create_session_factory, model_base


Base = model_base()


session_factory = create_session_factory(
    os.environ['DB_URI']
)

