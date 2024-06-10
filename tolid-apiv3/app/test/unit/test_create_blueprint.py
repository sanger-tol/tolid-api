# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock, create_autospec

from flask import Flask
from flask.testing import FlaskClient

import pytest

from tol.api_base2.misc import (
    AuthContext,
    CtxGetter
)
from tol.core import (
    DataObject,
    DataSource
)
from tol.core.operator import (
    Counter,
    Deleter,
    DetailGetter,
    PageGetter
)

from ...main.blueprint.create import (
    create_blueprint
)


@pytest.fixture(scope='function')
def auth_context() -> AuthContext:
    return create_autospec(
        AuthContext,
        spec_set=True
    )


@pytest.fixture(scope='function')
def ctx_getter(
    auth_context: AuthContext
) -> CtxGetter:

    mock_ctx_getter = Mock(spec_set=True)
    mock_ctx_getter.return_value = auth_context

    return mock_ctx_getter


@pytest.fixture
def mock_obj() -> DataObject:
    mock_obj = create_autospec(DataObject, spec_set=True)
    mock_obj.attributes = {}
    mock_obj.type = 'a'
    mock_obj.id = '999999'

    return mock_obj


@pytest.fixture
def mock_ds(mock_obj: DataObject) -> DataSource:

    class _MockDs(
        Counter,
        DataSource,
        DetailGetter,
        Deleter,
        PageGetter
    ):
        pass

    _mock = create_autospec(_MockDs, spec_set=True)
    _mock.supported_types = ['specimen', 'request']
    _mock.get_attribute_types.return_value = {}

    _mock.get_by_id.return_value = [mock_obj]
    _mock.get_page_size.return_value = 10
    _mock.get_list_page.return_value = ([], 0)

    _mock.get_session.return_value.get_count.return_value = 0

    return _mock


@pytest.fixture
def app(mock_ds: DataSource, ctx_getter: CtxGetter) -> Flask:
    app_fixture = Flask(__name__)
    create_bp = create_blueprint(
        mock_ds,
        url_prefix='/custom/create',
        ctx_getter=ctx_getter)
    app_fixture.register_blueprint(create_bp)
    return app_fixture


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


class TestCreateBlueprint:

    def test_create_request(
        self,
        client: FlaskClient,
        auth_context: AuthContext
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []

        response = client.post(
            '/custom/create/request',
            json=[{
                'species_id': '1234',
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_species_id': '5678'
            }]
        )
        assert response.status_code == 200
