# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from flask import Flask

from main.model import Base, UserMixin, main_models

from tol.api_base2 import data_blueprint, system_blueprint
from tol.core import core_data_object
from tol.sources.goat import goat
from tol.sql import create_sql_datasource
from tol.sql.auth import db_auth_blueprint

from .auth import create_auth_inspector


def application() -> Flask:
    app = Flask(__name__)

    db_uri = os.environ['DB_URI']
    api_path = os.environ['API_PATH']

    auth_bp = db_auth_blueprint(
        Base,
        db_uri,
        user_mixin_class=UserMixin,
        url_prefix=f'{api_path}/auth'
    )
    auth_bp.register_authenticator(app)
    app.register_blueprint(auth_bp)

    system_bp = system_blueprint(
        url_prefix=f'{api_path}/system'
    )
    app.register_blueprint(system_bp)

    User = auth_bp.models.user_class  # noqa
    sql_ds = create_sql_datasource(
        [
            User,
            *main_models
        ],
        db_uri,
        behind_api=True  # TODO is this right?
    )
    core_data_object(sql_ds)

    data_bp = data_blueprint(
        sql_ds,
        goat(),
        url_prefix=f'{api_path}',
        auth_inspector=create_auth_inspector()
    )
    app.register_blueprint(data_bp)

    return app
