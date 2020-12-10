# coding: utf-8
# ToDo not implemented yet!
from __future__ import absolute_import

from swagger_server.test import BaseTestCase

class TestConsumersController(BaseTestCase):

    def test_search_public_name(self):
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
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not correct for specimen
        query_string = [('taxonomyId', '9606'),
                        ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Specimen ID not in database
        query_string = [('taxonomyId', '6344'),
                        ('specimenId', 'SAN0000100zzzzz')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals([], response.json)

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
            "kingdom": "Metazoa",
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

        # Same again
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        self.assertEquals(expect, response.json)

    def test_bulk_search_public_name(self):
        # No authorisation token given
        body = []
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": "12345678"},
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        body = [{}]
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        body = [{'taxonomyId': 6344}]
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        body = [{'taxonomyId': 999999999,
                         'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        #TODO
        #self.assert400(response,
        #               'Response body is : ' + response.data.decode('utf-8'))

        # Specimen ID not in database - should create it
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100xxxxx'}]
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        expect = [{
            "commonName": "lugworm",
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "kingdom": "Metazoa",
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

        # Single search for existing
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        expect = [{
            "commonName": "lugworm",
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "kingdom": "Metazoa",
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

        # Search for existing and  2 new
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100wwwww'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100xxxxx'}]
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        expect = [{
            "commonName": "lugworm",
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "kingdom": "Metazoa",
            "prefix": "wuAreMari",
            "publicName": "wuAreMari1",
            "species": "Arenicola marina",
            "specimenId": "SAN0000100",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6344
        },
        {
            'commonName': 'lugworm',
            'family': 'Arenicolidae',
            'genus': 'Arenicola',
            'order': 'None',
            'phylum': 'Annelida',
            'kingdom': 'Metazoa',
            'prefix': 'wuAreMari',
            'publicName': 'wuAreMari3',
            'species': 'Arenicola marina',
            'specimenId': 'SAN0000100wwwww',
            'taxaClass': 'Polychaeta',
            'taxonomyId': 6344
        },
        {
            'commonName': 'lugworm',
            'family': 'Arenicolidae',
            'genus': 'Arenicola',
            'order': 'None',
            'phylum': 'Annelida',
            'kingdom': 'Metazoa',
            'prefix': 'wuAreMari',
            'publicName': 'wuAreMari4',
            'species': 'Arenicola marina',
            'specimenId': 'SAN0000100xxxxx',
            'taxaClass': 'Polychaeta',
            'taxonomyId': 6344
        }]

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Error on later query
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100bbbbb'},
                {'taxonomyId': 9606,
                'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/public_name_api/public-name',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)

        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # And the new one should not have been inserted
        query_string = [('taxonomyId', '6344'),
                        ('specimenId', 'SAN0000100bbbbb')]
        response = self.client.open(
            '/public_name_api/public-name',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals([], response.json)

    def test_search_species(self):
        # No taxonomyId given
        query_string = []
        response = self.client.open(
            '/public_name_api/species',
            method='GET',
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        query_string = [('taxonomyId', '999999999')]
        response = self.client.open(
            '/public_name_api/species',
            method='GET',
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # All data given
        query_string = [('taxonomyId', '6344')]
        response = self.client.open(
            '/public_name_api/species',
            method='GET',
            query_string=query_string)
        expect = [{
            "commonName": "lugworm",
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "kingdom": "Metazoa",
            "prefix": "wuAreMari",
            "species": "Arenicola marina",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6344
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Same again
        response = self.client.open(
            '/public_name_api/species',
            method='GET',
            query_string=query_string)
        self.assertEquals(expect, response.json)

if __name__ == '__main__':
    import unittest
    unittest.main()
