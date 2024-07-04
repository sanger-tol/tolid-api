# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from unittest.mock import create_autospec

import pytest

from tol.core import (
    DataObject,
)
from tol.core.operator import Relational

from ...main.util import (
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
    mock_obj.specimens = [
        mock_tolid1,
        mock_tolid2
    ]

    return mock_obj


class TestUtil:

    def test_current_highest_tolid_number(self, mock_species: DataObject):
        assert current_highest_tolid_number(mock_species) == 3
