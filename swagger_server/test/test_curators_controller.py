# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCuratorsController(BaseTestCase):
    """CuratorsController integration test stubs"""

    def test_add_public_name(self):
        """Test case for add_public_name

        adds a public name
        """
        body = PublicName()
        response = self.client.open(
            '/public-name',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
