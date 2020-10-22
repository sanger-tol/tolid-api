# coding: utf-8
# ToDo not implemented yet!
from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.public_name import PublicName  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCuratorsController(BaseTestCase):
    """CuratorsController integration test stubs"""

    def test_add_public_name(self):
        # No authorisation token given
        query_string = []
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            query_string=query_string)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        query_string = []
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": "12345678"},
            query_string=query_string)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        query_string = []
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        query_string = [('taxonomyId', 6344)]
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        query_string = [('taxonomyId', 999999999),
                         ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not correct for specimen
        query_string = [('taxonomyId', '9606'),
                        ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Specimen ID not in database - should create it
        query_string = [('taxonomyId', 6344),
                ('specimenId', 'SAN0000100xxxxx')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        expect = [{
            "commonName": "lugworm",
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "prefix": "wuAreMari",
            "publicName": "wuAreMari2",
            "species": "Arenicola marina",
            "specimenId": "SAN0000100xxxxx",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6344
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Specimen ID not in database and first for species - should create it
        query_string = [('taxonomyId', 9606),
                ('specimenId', 'SAN0000999xxxxx')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        expect = [{
            "commonName": "human",
            "family": "Hominidae",
            "genus": "Homo",
            "order": "Primates",
            "phylum": "Chordata",
            "prefix": "mHomSap",
            "publicName": "mHomSap1",
            "species": "Homo sapiens",
            "specimenId": "SAN0000999xxxxx",
            "taxaClass": "Mammalia",
            "taxonomyId": 9606
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Existing - should return existing
        query_string = [('taxonomyId', 6344),
                ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='PUT',
            headers={"api-key": self.api_key},
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
