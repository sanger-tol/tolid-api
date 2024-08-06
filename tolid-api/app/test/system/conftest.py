# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os
import pathlib
from datetime import timedelta

from flask import testing

import pytest

from sqlalchemy import Connection, create_engine

from tol.core import DataSource, core_data_object
from tol.sql import create_sql_datasource
from tol.sql.auth.models import create_models

from werkzeug.datastructures import Headers

from .data_objects import (
    create_test_data,
    delete_test_data
)
from ...main import application
from ...main.model import Base, UserMixin, main_models


@pytest.fixture(scope='session')
def api_path():
    return os.getenv('API_PATH', '/api/v3')


@pytest.fixture(scope='session')
def data_dir():
    """
    The directory where test data checked in to version control is stored.
    """
    return pathlib.Path(__file__).parent / 'data'


@pytest.fixture(scope='session')
def token() -> str:
    return 'Random'


@pytest.fixture(scope='module')
def auth_models():
    yield create_models(
        model_base=Base,
        user_table_name='user',
        oidc_id_column_name='email',
        user_mixin_class=UserMixin,
        token_expiry_delta=timedelta(days=1)
    )


@pytest.fixture(scope='module')
def sqla_engine():
    db_uri = os.getenv('DB_URI')
    assert db_uri
    engine = create_engine(db_uri)
    yield engine


@pytest.fixture(scope='module')
def sqla_connection(sqla_engine, auth_models):
    connection = sqla_engine.connect()
    Base.metadata.create_all(connection)
    connection.commit()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def sql_datasource(token: str, sqla_engine, sqla_connection: Connection, auth_models):
    sql_datasource = create_sql_datasource(
        [
            auth_models.user_class,
            auth_models.token_class,
            auth_models.role_class,
            auth_models.role_binding_class,
            *main_models
        ],
        os.getenv('DB_URI'),
        behind_api=False,  # TODO is this right?
    )
    core_data_object(sql_datasource)
    delete_test_data(sqla_connection, auth_models)
    create_test_data(sql_datasource, token)
    yield sql_datasource
    delete_test_data(sqla_engine, auth_models)


@pytest.fixture
def flask_app(sql_datasource: DataSource):
    app = application()
    app.testing = True
    yield app


@pytest.fixture()
def client(flask_app, token):

    class TestClient(testing.FlaskClient):
        def open(self, *args, **kwargs):  # noqa: A003
            headers = kwargs.setdefault('headers', Headers())
            headers.add('token', token)
            return super().open(*args, **kwargs)

    flask_app.test_client_class = TestClient
    return flask_app.test_client()
