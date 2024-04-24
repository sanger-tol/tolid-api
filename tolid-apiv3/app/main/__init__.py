# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from flask import Flask

from tol.api_base2 import data_blueprint
from tol.core import core_data_object
from tol.sql import create_sql_datasource
from tol.sql.auth import db_auth_blueprint

from main.model import Base, UserMixin, main_models


def application() -> Flask:
    app = Flask(__name__)

    DB_URI = os.environ['DB_URI']
    API_PATH = os.environ['API_PATH']

    auth_bp = db_auth_blueprint(
        Base,
        DB_URI,
        user_mixin_class=UserMixin,
        url_prefix=f'{API_PATH}/auth'
    )
    auth_bp.register_authenticator(app)
    app.register_blueprint(auth_bp)

    User = auth_bp.models.user_class  # noqa
    sql_ds = create_sql_datasource(
        [
            User,
            *main_models
        ],
        DB_URI,
        behind_api=True  # TODO is this right?
    )
    core_data_object(sql_ds)

    data_bp = data_blueprint(
        sql_ds,
        url_prefix=f'{API_PATH}/data'
    )
    app.register_blueprint(data_bp)

    return app
