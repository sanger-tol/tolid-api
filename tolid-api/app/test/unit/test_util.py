# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from unittest.mock import create_autospec

import pytest

from tol.core import (
    DataObject,
    DataSource
)
from tol.core.operator import Relational

from ...main.util import (
    create_new_tolid,
    current_highest_tolid_number
)


@pytest.fixture
def mock_species() -> DataObject:
    class __CombinedClass(DataObject, Relational):
        pass

    mock_tolid1 = create_autospec(DataObject)
    mock_tolid1.number = 1
    mock_tolid2 = create_autospec(DataObject)
    mock_tolid2.number = 3

    mock_obj = create_autospec(DataObject)
    mock_obj.attributes = {}
    mock_obj.type = 'species'
    mock_obj.id = '999999'
    mock_obj.prefix = 'abCdeFghi'
    mock_obj.specimens = [
        mock_tolid1,
        mock_tolid2
    ]

    return mock_obj


@pytest.fixture
def mock_user() -> DataObject:
    mock_user = create_autospec(DataObject)
    mock_user.id = 100
    return mock_user


@pytest.fixture
def mock_ds() -> DataSource:

    class _MockDs(
        DataSource,
    ):
        pass

    _mock = create_autospec(_MockDs, spec_set=True)
    _mock.supported_types = ['specimen', 'request']

    mock_session_context = _mock.get_session.return_value.__enter__.return_value
    mock_session_context.get_count.return_value = 0

    return _mock


class TestUtil:

    def test_current_highest_tolid_number(self, mock_species: DataObject, mock_user: DataObject):
        assert current_highest_tolid_number(mock_species) == 3

    def test_create_new_tolid(
        self,
        mock_species: DataObject,
        mock_ds: DataSource,
        mock_user: DataObject
    ):
        mock_session_context = mock_ds.get_session.return_value.__enter__.return_value
        create_new_tolid(
            mock_session_context,
            mock_species,
            'ABC123',
            5678,
            mock_user
        )
        args, kwargs = mock_session_context.data_object_factory.call_args_list[0]
        assert args[0] == 'specimen'
        assert args[1] == 'abCdeFghi4'
        assert kwargs['attributes']['requested_taxonomy_id'] == 5678
        assert kwargs['attributes']['specimen_id'] == 'ABC123'
        assert kwargs['attributes']['number'] == 4
