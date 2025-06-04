# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import os
import pathlib
from typing import Iterator

from flask import Flask, testing

import pytest

from sqlalchemy import create_engine

from tol.core import DataSource, core_data_object
from tol.sql import create_sql_datasource
from tol.sql.auth import DbAuthBlueprint

from werkzeug.datastructures import Headers

from .data_objects import (
    create_test_data,
    delete_test_data
)
from ...main import Base, application, get_auth_bp, main_models


def __set_up(db_uri: str) -> None:
    engine = create_engine(db_uri)
    try:
        Base.metadata.create_all(engine)
    except:  # noqa
        pass


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


@pytest.fixture(scope='session')
def db_uri() -> str:
    return os.environ['DB_URI']


@pytest.fixture(scope='session')
def url_prefix(
    api_path: str,
) -> str:

    api_system_path = os.getenv('API_SYSTEM_PATH', '/system')

    return f'{api_path}{api_system_path}'


@pytest.fixture(scope='session')
def auth_bp(
    db_uri: str,
    url_prefix: str,
) -> DbAuthBlueprint:

    return get_auth_bp(
        Base,
        db_uri,
        url_prefix,
    )


@pytest.fixture(autouse=True)
def full_models_list(
    auth_bp: DbAuthBlueprint,
    db_uri: str,
):

    __set_up(db_uri)

    return [
        *main_models,
        *auth_bp.models,
    ]


@pytest.fixture
def sql_datasource(
    db_uri: str,
    token: str,
    full_models_list: list,
) -> DataSource:

    sql_datasource = create_sql_datasource(
        full_models_list,
        db_uri,
        behind_api=False,  # TODO is this right?
    )
    core_data_object(sql_datasource)
    delete_test_data(sql_datasource, full_models_list)
    create_test_data(sql_datasource, token)
    yield sql_datasource
    delete_test_data(sql_datasource, full_models_list)


@pytest.fixture
def flask_app(
    auth_bp: DbAuthBlueprint,
) -> Iterator[Flask]:

    app = application(
        auth_bp=auth_bp,
    )
    app.testing = True
    yield app


@pytest.fixture
def client(
    flask_app: Flask,
    token: str,
) -> testing.FlaskClient:

    class TestClient(testing.FlaskClient):
        def open(self, *args, **kwargs):  # noqa: A003
            headers = kwargs.setdefault('headers', Headers())
            headers.add('token', token)
            return super().open(*args, **kwargs)

    flask_app.test_client_class = TestClient
    return flask_app.test_client()
