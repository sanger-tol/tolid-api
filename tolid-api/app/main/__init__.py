# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os

from flask import Flask

from main.blueprint import request_blueprint
from main.model import Base, UserMixin, main_models

from tol.api_base import data_blueprint, system_blueprint
from tol.core import core_data_object
from tol.sources.goat import goat
from tol.sql import create_sql_datasource
from tol.sql.auth import db_auth_blueprint

from .auth import create_auth_inspector


def application() -> Flask:
    app = Flask(__name__)

    db_uri = os.environ['DB_URI']
    api_path = os.getenv('API_PATH', '/api/v3')
    api_data_path = os.getenv('API_DATA_PATH', '/data')
    api_system_path = os.getenv('API_SYSTEM_PATH', '/system')
    api_auth_path = os.getenv('API_AUTH_PATH', '/auth')
    api_custom_path = os.getenv('API_CUSTOM_PATH', '/')

    auth_bp = db_auth_blueprint(
        Base,
        db_uri,
        user_mixin_class=UserMixin,
        url_prefix=f'{api_path}{api_auth_path}',
        oidc_id_column_name='email',
        oidc_ext_mapping={'name': 'name'},
    )
    auth_bp.register_authenticator(app)
    app.register_blueprint(auth_bp)

    system_bp = system_blueprint(
        url_prefix=f'{api_path}{api_system_path}'
    )
    app.register_blueprint(system_bp)

    User = auth_bp.models.user_class  # noqa

    sql_ds = create_sql_datasource(
        [
            User,
            *main_models
        ],
        db_uri,
        behind_api=True,  # TODO is this right?
    )
    core_data_object(sql_ds)

    goat_ds = goat()

    data_bp = data_blueprint(
        sql_ds,
        goat_ds,
        url_prefix=f'{api_path}{api_data_path}',
        auth_inspector=create_auth_inspector()
    )
    app.register_blueprint(data_bp)

    request_bp = request_blueprint(
        sql_ds,
        goat_ds,
        url_prefix=f'{api_path}{api_custom_path}/request'
    )
    app.register_blueprint(request_bp)

    return app
