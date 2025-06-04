# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock, create_autospec

from flask import Flask
from flask.testing import FlaskClient

import pytest

from tol.api_base.misc import (
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
    PageGetter,
    Relational
)
from tol.core.relationship import RelationshipConfig

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
    mock_obj = create_autospec(DataObject)
    mock_obj.attributes = {}
    mock_obj.type = 'request'
    mock_obj.id = '999999'
    mock_obj.specimen_id = 'ABC123'
    mock_obj.requested_taxonomy_id = 5678
    mock_obj.species_id = 1234

    return mock_obj


@pytest.fixture
def mock_tolid_species() -> DataObject:
    mock_obj = create_autospec(DataObject)
    mock_obj.attributes = {}
    mock_obj.type = 'species'
    mock_obj.id = 1234

    return mock_obj


@pytest.fixture
def mock_species() -> DataObject:
    mock_obj = create_autospec(DataObject)
    mock_obj.attributes = {}
    mock_obj.type = 'taxon'
    mock_obj.id = '1234'
    mock_obj.rank = 'species'
    mock_obj.species = mock_obj

    return mock_obj


@pytest.fixture
def mock_subspecies(mock_species) -> DataObject:
    mock_obj = create_autospec(DataObject)
    mock_obj.attributes = {}
    mock_obj.type = 'taxon'
    mock_obj.id = '5678'
    mock_obj.rank = 'subspecies'
    mock_obj.species = mock_species

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
    _mock.supported_types = ['species', 'specimen', 'request']

    mock_session_context = _mock.get_session.return_value.__enter__.return_value
    mock_session_context.get_count.return_value = 0

    return _mock


@pytest.fixture
def mock_goat(mock_obj: DataObject) -> DataSource:

    class _MockDs(
        DataSource,
        DetailGetter,
        Relational
    ):
        pass

    _mock = create_autospec(_MockDs, spec_set=True)
    _mock.supported_types = ['taxon']

    @property
    def relationship_config(self):
        rc_taxon = RelationshipConfig()
        rc_taxon.to_one = {
            'species': 'taxon'
        }
        return {'taxon': rc_taxon}

    def get_to_one_relation(
        self,
        source: DataObject,
        relationship_name: str
    ):
        pass

    def get_to_many_relations(
        self
    ):
        raise NotImplementedError()

    return _mock


@pytest.fixture
def app(mock_ds: DataSource, mock_goat: DataSource, ctx_getter: CtxGetter) -> Flask:
    app_fixture = Flask(__name__)
    request_bp = request_blueprint(
        mock_ds,
        mock_goat,
        url_prefix='/custom/request',
        ctx_getter=ctx_getter)
    app_fixture.register_blueprint(request_bp)
    return app_fixture


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


class TestRequestBlueprint:

    def test_create_request_user_new_species(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject,
        mock_goat: DataSource,
        mock_subspecies: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.insert.return_value = [mock_obj]

        mock_session_context.get_one.return_value = None
        mock_goat.get_one.return_value = mock_subspecies

        response = client.post(
            '/custom/request/create',
            json=[{
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
        assert kwargs['attributes']['status'] == 'Pending'

    def test_create_request_user_existing_species(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject,
        mock_goat: DataSource,
        mock_tolid_species: DataObject,
        mock_species: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.insert.return_value = [mock_obj]

        mock_session_context.get_one.return_value = mock_tolid_species
        mock_goat.get_one.return_value = mock_species

        response = client.post(
            '/custom/request/create',
            json=[{
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 1234
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
        # assert kwargs['attributes']['requested_taxonomy_id'] == 5678
        assert kwargs['attributes']['specimen_id'] == 'ABC123'
        assert kwargs['attributes']['confirmation_name'] == 'Grubby grommitulus'
        assert kwargs['attributes']['status'] == 'Pending'

    def test_create_request_user_request_exists(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_goat: DataSource,
        mock_subspecies: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []
        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.get_count.return_value = 1

        mock_session_context.get_one.return_value = None
        mock_goat.get_one.return_value = mock_subspecies

        response = client.post(
            '/custom/request/create',
            json=[{
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 400

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.insert.call_count == 0

    def test_create_request_user_tolid_exists(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_goat: DataSource,
        mock_subspecies: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = []
        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.get_count.side_effect = [0, 1]

        mock_session_context.get_one.return_value = None
        mock_goat.get_one.return_value = mock_subspecies

        response = client.post(
            '/custom/request/create',
            json=[{
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 400

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.insert.call_count == 0

    def test_reject_request(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['admin']

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.upsert.return_value = [mock_obj]

        response = client.patch(
            '/custom/request/reject',
            json=[{
                'request_id': 999999,
                'reason': 'Not nice'
            }]
        )
        assert response.status_code == 200
        assert response.json == {'data': [{'id': '999999', 'type': 'request'}]}

        assert mock_session_context.data_object_factory.call_count == 1
        assert mock_session_context.upsert.call_count == 1
        assert mock_session_context.upsert.call_args[0][0] == 'request'
        mock_data_object_list = mock_session_context.upsert.call_args[0][1]
        assert len(mock_data_object_list) == 1

        args, kwargs = mock_session_context.data_object_factory.call_args_list[0]
        assert args[0] == 'request'
        assert args[1] == 999999
        assert kwargs['attributes']['reason'] == 'Not nice'
        assert kwargs['attributes']['status'] == 'Rejected'

    def test_reject_request_not_found(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['admin']

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.get_one.return_value = None

        response = client.patch(
            '/custom/request/reject',
            json=[{
                'request_id': 999999,
                'reason': 'Not nice'
            }]
        )
        assert response.status_code == 400

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.upsert.call_count == 0

    def test_accept_request(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['admin']

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value

        mock_user = create_autospec(DataObject)
        mock_user.id = 1
        mock_obj.user = mock_user

        mock_specimen1 = create_autospec(DataObject)
        mock_specimen1.number = 1
        mock_specimen2 = create_autospec(DataObject)
        mock_specimen2.number = 3

        mock_species = create_autospec(DataObject)
        mock_species.attributes = {}
        mock_species.type = 'species'
        mock_species.id = 1234
        mock_species.prefix = 'abCdeFghi'
        mock_species.specimens = [mock_specimen1, mock_specimen2]
        mock_session_context.get_one.side_effect = [mock_obj, mock_species]

        mock_specimen3 = create_autospec(DataObject)
        mock_specimen3.number = 4
        mock_specimen3.id = 'abCdeFghi4'
        mock_specimen3.type = 'specimen'
        mock_specimen3.species = mock_species
        mock_specimen3.specimen_id = 'ABC123'

        mock_session_context.insert.return_value = [mock_specimen3]

        response = client.patch(
            '/custom/request/accept',
            json=[{
                'request_id': 999999
            }]
        )
        assert response.status_code == 200
        assert response.json == {'data': [{
            'id': 'abCdeFghi4',
            'type': 'specimen',
            'attributes': {}
        }]}

        assert mock_session_context.data_object_factory.call_count == 1
        assert mock_session_context.insert.call_count == 1
        assert mock_session_context.insert.call_args[0][0] == 'specimen'
        mock_data_object_list = mock_session_context.insert.call_args[0][1]
        assert len(mock_data_object_list) == 1

        args, kwargs = mock_session_context.data_object_factory.call_args_list[0]
        assert args[0] == 'specimen'
        assert args[1] == 'abCdeFghi4'
        assert kwargs['attributes']['specimen_id'] == 'ABC123'
        assert kwargs['attributes']['number'] == 4
        assert kwargs['attributes']['requested_taxonomy_id'] == 5678
        assert kwargs['to_one']['species'] == mock_species
        assert kwargs['to_one']['user'] == mock_user

        assert mock_session_context.delete.call_count == 1
        assert mock_session_context.delete.call_args[0][0] == 'request'
        mock_object_id_list = mock_session_context.delete.call_args[0][1]
        assert len(mock_object_id_list) == 1
        assert mock_object_id_list[0] == '999999'

    def test_accept_request_not_found(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['admin']

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.get_one.return_value = None

        response = client.patch(
            '/custom/request/accept',
            json=[{
                'request_id': 999999
            }]
        )
        assert response.status_code == 400

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.upsert.call_count == 0

    def test_accept_species_not_found(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_obj: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['admin']

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        mock_session_context.get_one.side_effect = [mock_obj, None]

        response = client.patch(
            '/custom/request/accept',
            json=[{
                'request_id': 999999
            }]
        )
        assert response.status_code == 400

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.upsert.call_count == 0

    def test_create_request_creator(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_goat: DataSource,
        mock_obj: DataObject,
        mock_tolid_species: DataObject,
        mock_species: DataObject,
        mock_subspecies: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['creator']

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value

        mock_user = create_autospec(DataObject)
        mock_user.id = 100
        mock_obj.user = mock_user

        mock_specimen1 = create_autospec(DataObject)
        mock_specimen1.number = 1
        mock_specimen2 = create_autospec(DataObject)
        mock_specimen2.number = 3

        mock_tolid_species.attributes = {}
        mock_tolid_species.prefix = 'abCdeFghi'
        mock_tolid_species.specimens = [mock_specimen1, mock_specimen2]
        mock_session_context.get_one.side_effect = [
            None, mock_tolid_species,  # validation
            mock_user, None, mock_tolid_species,  # first request
            mock_user, mock_tolid_species, mock_tolid_species  # second request
        ]

        mock_specimen3 = create_autospec(DataObject)
        mock_specimen3.number = 4
        mock_specimen3.id = 'abCdeFghi4'
        mock_specimen3.type = 'specimen'
        mock_specimen3.species = mock_tolid_species
        mock_specimen3.specimen_id = 'ABC123'
        mock_specimen4 = create_autospec(DataObject)
        mock_specimen4.number = 5
        mock_specimen4.id = 'abCdeFghi5'
        mock_specimen4.type = 'specimen'
        mock_specimen4.species = mock_tolid_species
        mock_specimen4.specimen_id = 'ABC456'

        mock_session_context.insert.side_effect = [[mock_specimen3], [mock_specimen4]]

        mock_goat.get_one.side_effect = [mock_subspecies, mock_subspecies]

        response = client.post(
            '/custom/request/create',
            json=[{
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }, {
                'requested_taxonomy_id': 1234,
                'specimen_id': 'ABC456'
            }]
        )
        assert response.status_code == 200
        assert response.json == {'data': [
            {
                'id': 'abCdeFghi4',
                'type': 'specimen',
                'attributes': {
                    # Attributes don't work quite the same with mocks
                }
            }, {
                'id': 'abCdeFghi5',
                'type': 'specimen',
                'attributes': {
                    # Attributes don't work quite the same with mocks
                }
            }
        ]}
        assert mock_session_context.data_object_factory.call_count == 2
        assert mock_session_context.insert.call_count == 2
        assert mock_session_context.insert.call_args[0][0] == 'specimen'
        mock_data_object_list = mock_session_context.insert.call_args[0][1]
        assert len(mock_data_object_list) == 1

        args, kwargs = mock_session_context.data_object_factory.call_args_list[0]
        assert args[0] == 'specimen'
        assert args[1] == 'abCdeFghi4'
        assert kwargs['attributes']['requested_taxonomy_id'] == 5678
        assert kwargs['attributes']['specimen_id'] == 'ABC123'
        assert kwargs['attributes']['number'] == 4
        assert kwargs['to_one']['species'] == mock_tolid_species
        assert kwargs['to_one']['user'] == mock_user

        args, kwargs = mock_session_context.data_object_factory.call_args_list[1]
        assert args[0] == 'specimen'
        assert args[1] == 'abCdeFghi4'  # Would have incremented
        assert kwargs['attributes']['requested_taxonomy_id'] == 1234
        assert kwargs['attributes']['specimen_id'] == 'ABC456'
        assert kwargs['attributes']['number'] == 4  # Would have incremented
        assert kwargs['to_one']['species'] == mock_tolid_species
        assert kwargs['to_one']['user'] == mock_user

    def test_create_request_creator_tolid_exists(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_goat: DataSource,
        mock_tolid_species: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['creator']
        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value

        mock_specimen1 = create_autospec(DataObject)
        mock_specimen1.id = 'abCdeFghi1'
        mock_specimen1.type = 'specimen'
        mock_specimen1.specimen_id = 'ABC123'
        mock_specimen1.number = 1

        mock_tolid_species.prefix = 'abCdeFghi'
        mock_tolid_species.specimens = [mock_specimen1]

        mock_session_context.get_one.side_effect = [mock_tolid_species,  # validation
                                                    None, mock_tolid_species]

        mock_session_context.get_list.return_value = [mock_specimen1]

        mock_goat.get_one.side_effect = [mock_subspecies]

        response = client.post(
            '/custom/request/create',
            json=[{
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 200
        assert response.json == {'data': [
            {
                'id': 'abCdeFghi1',
                'type': 'specimen',
                'attributes': {
                    # Attributes don't work quite the same with mocks
                }
            }
        ]}

        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.insert.call_count == 0

    def test_create_request_creator_no_species_request_exists(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_goat: DataSource,
        mock_obj: DataObject,
        mock_tolid_species: DataObject,
        mock_subspecies: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['creator']

        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value

        mock_session_context.get_one.side_effect = [None,  # validation
                                                    None, mock_tolid_species]
        mock_session_context.get_list.return_value = [mock_obj]

        mock_goat.get_one.side_effect = [mock_subspecies]

        response = client.post(
            '/custom/request/create',
            json=[{
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 200
        assert response.json == {'data': [
            {
                'id': '999999',
                'type': 'request'
            }
        ]}
        assert mock_session_context.data_object_factory.call_count == 0
        assert mock_session_context.insert.call_count == 0

    def test_create_request_creator_no_species_request_not_exists(
        self,
        client: FlaskClient,
        auth_context: AuthContext,
        mock_ds: DataSource,
        mock_goat: DataSource,
        mock_obj: DataObject,
        mock_tolid_species: DataObject,
        mock_subspecies: DataObject
    ):
        auth_context.authenticated = True
        auth_context.user_id = '100'
        auth_context.roles = ['creator']
        mock_user = create_autospec(DataObject)
        mock_user.id = 100
        mock_obj.user = mock_user
        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value

        mock_session_context.get_one.side_effect = [None,  # validation
                                                    None, mock_tolid_species]
        mock_session_context.get_list.return_value = []

        mock_session_context.insert.return_value = [mock_obj]

        mock_goat.get_one.side_effect = [mock_subspecies]

        response = client.post(
            '/custom/request/create',
            json=[{
                'specimen_id': 'ABC123',
                'species_name': 'Grubby grommitulus',
                'requested_taxonomy_id': 5678
            }]
        )
        assert response.status_code == 200
        assert response.json == {'data': [
            {
                'id': '999999',
                'type': 'request'
            }
        ]}
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
        assert kwargs['attributes']['status'] == 'Pending'
