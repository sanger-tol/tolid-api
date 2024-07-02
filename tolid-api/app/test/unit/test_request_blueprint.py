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

from ...main.blueprint.request import (
    request_blueprint
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
    mock_obj.type = 'request'
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

    mock_session_context = _mock.get_session.return_value.__enter__.return_value
    mock_session_context.get_count.return_value = 0

    return _mock


@pytest.fixture
def app(mock_ds: DataSource, ctx_getter: CtxGetter) -> Flask:
    app_fixture = Flask(__name__)
    request_bp = request_blueprint(
        mock_ds,
        url_prefix='/custom/request',
        ctx_getter=ctx_getter)
    app_fixture.register_blueprint(request_bp)
    return app_fixture


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


class TestRequestBlueprint:

    def test_create_request(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.insert.return_value = [mock_obj]

        response = client.post(
            '/custom/request/create',
            json=[{
                'species_id': 1234,
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 200
        assert response.json == {'data': [{'id': '999999', 'type': 'request'}]}

        assert mock_session_context.data_object_factory.call_count == 1
        assert mock_session_context.insert.call_count == 1
        assert mock_session_context.insert.call_args[0][0] == 'request'
        mock_data_object_list = mock_session_context.insert.call_args[0][1]
        assert len(mock_data_object_list) == 1

        args, kwargs = mock_session_context.data_object_factory.call_args_list[0]
        assert args[0] == 'request'
        assert args[1] is None
        assert kwargs['attributes']['species_id'] == 1234
        assert kwargs['attributes']['requested_taxonomy_id'] == 5678
        assert kwargs['attributes']['specimen_id'] == 'ABC123'
        assert kwargs['attributes']['confirmation_name'] == 'Grubby grommitulus'
        assert kwargs['attributes']['status'] == 'Pre-pending'

    def test_create_request_exists(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []
        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.get_count.return_value = 1

        response = client.post(
            '/custom/request/create',
            json=[{
                'species_id': 1234,
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 400

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.insert.call_count == 0

    def test_create_tolid_exists(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []
        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.get_count.side_effect = [0, 1]

        response = client.post(
            '/custom/request/create',
            json=[{
                'species_id': 1234,
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 400

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.insert.call_count == 0
