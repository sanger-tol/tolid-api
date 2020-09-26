# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server.test import BaseTestCase


class TestConsumersController(BaseTestCase):
    """ConsumersController integration test stubs"""

    def test_search_public_name(self):
        """Test case for search_public_name

        searches DToL public names
        """
        query_string = [('search_string', 'search_string_example'),
                        ('skip', 1),
                        ('limit', 10000000)]
        response = self.client.open(
            '/public-name',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
