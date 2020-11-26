# coding: utf-8
# ToDo not implemented yet!
from __future__ import absolute_import

from swagger_server.test import BaseTestCase

from swagger_server.db_utils import create_new_specimen

class TestDbUtils(BaseTestCase):
    """CuratorsController integration test stubs"""

    def test_create_new_specimen(self):
        # No authorisation token given
        new_specimen = create_new_specimen(self.species1, "TEST12345678", self.user1)
        self.assertEqual(new_specimen.specimen_id, "TEST12345678")
        self.assertEqual(new_specimen.species, self.species1)
        self.assertEqual(new_specimen.user, self.user1)
        self.assertEqual(new_specimen.number, 2)


if __name__ == '__main__':
    import unittest
    unittest.main()
