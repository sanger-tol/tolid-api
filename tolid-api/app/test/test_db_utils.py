from __future__ import absolute_import

from test import BaseTestCase

from main.db_utils import create_new_specimen, accept_request, \
    reject_request, create_request
from main.model import db, TolidRequest


class TestDbUtils(BaseTestCase):
    """CuratorsController integration test stubs"""

    def test_create_new_specimen(self):
        # No authorisation token given
        new_specimen = create_new_specimen(self.species1, "TEST12345678", self.user1)
        self.assertEqual(new_specimen.specimen_id, "TEST12345678")
        self.assertEqual(new_specimen.species, self.species1)
        self.assertEqual(new_specimen.user, self.user1)
        self.assertEqual(new_specimen.number, 3)

    def test_accept_request(self):
        self.request1 = TolidRequest(specimen_id="SAN0000100xxxxx",
                                     species_id=999999, status="Pending")
        self.request1.user = self.user1
        db.session.add(self.request1)

        try:
            accept_request(self.request1)
            self.assertTrue(False)
        except Exception:
            pass

        self.request1.species_id = 6344
        tol_id = accept_request(self.request1)
        self.assertEqual(tol_id.user, self.user1)
        self.assertEqual(tol_id.tolid, 'wuAreMari3')
        # Check the original request has been deleted
        request = db.session.query(TolidRequest).filter(TolidRequest.request_id == 1).one_or_none()
        self.assertIsNone(request)

    def test_reject_request(self):
        self.request1 = TolidRequest(specimen_id="SAN0000100xxxxx",
                                     species_id=6344, status="Pending",
                                     reason="Invalid")
        self.request1.user = self.user1
        db.session.add(self.request1)

        request = reject_request(self.request1, 'Invalid')
        self.assertEqual(request.status, 'Rejected')
        self.assertEqual(request.reason, 'Invalid')

    def test_create_request(self):
        new_request = create_request(self.species1.taxonomy_id, "TEST44444", self.user1)
        self.assertEqual(new_request.specimen_id, "TEST44444")
        self.assertEqual(new_request.species_id, self.species1.taxonomy_id)
        self.assertEqual(new_request.user, self.user1)
        self.assertEqual(new_request.status, "Pre-pending")


if __name__ == '__main__':
    import unittest
    unittest.main()
