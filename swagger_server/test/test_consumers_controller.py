# coding: utf-8
# ToDo not implemented yet!
from __future__ import absolute_import

from swagger_server.test import BaseTestCase

class TestConsumersController(BaseTestCase):

    def test_search_specimen(self):

        # Specimen ID not in database
        response = self.client.open(
            '/api/v2/specimens/SAN0000100zzzzz',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals([], response.json)

        # All data given
        response = self.client.open(
            '/api/v2/specimens/SAN0000100',
            method='GET')
        expect = [{
            "specimenId": "SAN0000100",
            "tolIds": [
                {
                    "tolId": "wuAreMari1",
                    "species":{
                        "commonName": "lugworm",
                        "family": "Arenicolidae",
                        "genus": "Arenicola",
                        "order": "None",
                        "phylum": "Annelida",
                        "kingdom": "Metazoa",
                        "prefix": "wuAreMari",
                        "scientificName": "Arenicola marina",
                        "taxaClass": "Polychaeta",
                        "taxonomyId": 6344
                    }
                }
            ]
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/specimens/SAN0000100',
            method='GET')
        self.assertEquals(expect, response.json)

    def test_search_tol_id(self):

        # ToLID not in database
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari99999',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals([], response.json)

        # All data given
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari1',
            method='GET')
        expect = [{
            "species":{
                "commonName": "lugworm",
                "family": "Arenicolidae",
                "genus": "Arenicola",
                "order": "None",
                "phylum": "Annelida",
                "kingdom": "Metazoa",
                "prefix": "wuAreMari",
                "scientificName": "Arenicola marina",
                "taxaClass": "Polychaeta",
                "taxonomyId": 6344
            },
            "tolId": "wuAreMari1",
            "specimen": {"specimenId": "SAN0000100"}
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari1',
            method='GET')
        self.assertEquals(expect, response.json)

    def test_bulk_search_tol_ids(self):
        # No authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/tol-ids',
            method='POST',
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={"api-key": "12345678"},
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        body = [{}]
        response = self.client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        body = [{'taxonomyId': 6344}]
        response = self.client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        body = [{'taxonomyId': 999999999,
                         'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/api/v2/tol-ids',
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
            '/api/v2/tol-ids',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        expect = [{
            "species": {
                "commonName": "lugworm",
                "family": "Arenicolidae",
                "genus": "Arenicola",
                "order": "None",
                "phylum": "Annelida",
                "kingdom": "Metazoa",
                "prefix": "wuAreMari",
                "scientificName": "Arenicola marina",
                "taxaClass": "Polychaeta",
                "taxonomyId": 6344
            },
            "tolId": "wuAreMari2",
            "specimen": {"specimenId": "SAN0000100xxxxx"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Single search for existing
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        expect = [{
            "species": {
                "commonName": "lugworm",
                "family": "Arenicolidae",
                "genus": "Arenicola",
                "order": "None",
                "phylum": "Annelida",
                "kingdom": "Metazoa",
                "prefix": "wuAreMari",
                "scientificName": "Arenicola marina",
                "taxaClass": "Polychaeta",
                "taxonomyId": 6344
            },
            "tolId": "wuAreMari1",
            "specimen": {"specimenId": "SAN0000100"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Search for existing and new
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100wwwww'}]
        response = self.client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)
        expect = [{
            "species": {
                "commonName": "lugworm",
                "family": "Arenicolidae",
                "genus": "Arenicola",
                "order": "None",
                "phylum": "Annelida",
                "kingdom": "Metazoa",
                "prefix": "wuAreMari",
                "scientificName": "Arenicola marina",
                "taxaClass": "Polychaeta",
                "taxonomyId": 6344
            },
            "tolId": "wuAreMari1",
            "specimen": {"specimenId": "SAN0000100"},
        },
        {
            'species': {
                'commonName': 'lugworm',
                'family': 'Arenicolidae',
                'genus': 'Arenicola',
                'order': 'None',
                'phylum': 'Annelida',
                'kingdom': 'Metazoa',
                'prefix': 'wuAreMari',
                'scientificName': 'Arenicola marina',
                'taxaClass': 'Polychaeta',
                'taxonomyId': 6344
            },
            'tolId': 'wuAreMari3',
            'specimen': {'specimenId': 'SAN0000100wwwww'},
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
            '/api/v2/tol-ids',
            method='POST',
            headers={"api-key": self.api_key},
            json=body)

        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # And the new one should not have been inserted
        response = self.client.open(
            '/api/v2/specimens/SAN0000100bbbbb',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals([], response.json)

    def test_search_species(self):
        # Taxonomy ID not in database
        response = self.client.open(
            '/api/v2/species/999999999',
            method='GET')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # All data given
        response = self.client.open(
            '/api/v2/species/6344',
            method='GET')
        expect = [{
            "commonName": "lugworm",
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "kingdom": "Metazoa",
            "prefix": "wuAreMari",
            "scientificName": "Arenicola marina",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6344
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/species/6344',
            method='GET')
        self.assertEquals(expect, response.json)

if __name__ == '__main__':
    import unittest
    unittest.main()
