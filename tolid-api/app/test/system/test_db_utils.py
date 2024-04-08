# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from __future__ import absolute_import

import pytest

from main.db_utils import accept_request, create_new_specimen, \
    create_request, reject_request
from main.model import TolidRequest

from test.system.asserts import assertEqual


class TestDbUtils:
    """CuratorsController integration test stubs"""

    def test_create_new_specimen(self):
        # No authorisation token given
        new_specimen = create_new_specimen(self.species1, 'TEST12345678', self.user_requester)
        assertEqual(new_specimen.specimen_id, 'TEST12345678')
        assertEqual(new_specimen.species, self.species1)
        assertEqual(new_specimen.user, self.user_requester)
        assertEqual(new_specimen.number, 3)

    def test_accept_request(self, session):
        request1 = TolidRequest(specimen_id='SAN0000100xxxxx',
                                    species_id=999999, status='Pending')
        request1.user = self.user_requester
        session.add(request1)

        with pytest.raises(Exception):
            accept_request(request1)

        request1.species_id = 6344
        tol_id = accept_request(request1)
        assertEqual(tol_id.user, self.user_requester)
        assertEqual(tol_id.tolid, 'wuAreMari3')
        # Check the original request has been deleted
        request = session.query(TolidRequest).filter(TolidRequest.request_id == 1).one_or_none()
        assert request is None

    def test_reject_request(self, session):
        request1 = TolidRequest(specimen_id='SAN0000100xxxxx',
                                    species_id=6344, status='Pending',
                                    reason='Invalid')
        request1.user = self.user_requester
        session.add(request1)

        request = reject_request(request1, 'Invalid')
        assertEqual(request.status, 'Rejected')
        assertEqual(request.reason, 'Invalid')

    def test_create_request(self):
        new_request = create_request(self.species1.taxonomy_id, 'TEST44444', self.user_requester)
        assertEqual(new_request.specimen_id, 'TEST44444')
        assertEqual(new_request.species_id, self.species1.taxonomy_id)
        assertEqual(new_request.user, self.user_requester)
        assertEqual(new_request.status, 'Pre-pending')


if __name__ == '__main__':
    import unittest
    unittest.main()
