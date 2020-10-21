# coding: utf-8
# ToDo not implemented yet!
from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server.test import BaseTestCase


class TestConsumersController(BaseTestCase):
    """ConsumersController integration test stubs"""

    def setUp(self):
        #TODO
        pass

    def tearDown(self):
        #TODO
        pass

    def test_search_public_name(self):
        """Test case for search_public_name

        searches DToL public names
        """
        # No taxonomyId given
        query_string = []
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        query_string = [('taxonomyId', '6344')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        query_string = [('taxonomyId', '999999999'),
                        ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        #TODO
        #self.assert400(response,
        #               'Response body is : ' + response.data.decode('utf-8'))

        # All data given
        query_string = [('taxonomyId', '6344'),
                        ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        expect = [{
            "commonName": "lugworm",
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "prefix": "wuAreMari",
            "publicName": "wuAreMari1",
            "species": "Arenicola marina",
            "specimenId": "SAN0000100",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6344
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)


if __name__ == '__main__':
    import unittest
    unittest.main()
