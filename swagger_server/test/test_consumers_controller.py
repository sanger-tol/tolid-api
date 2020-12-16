# coding: utf-8
# ToDo not implemented yet!
from __future__ import absolute_import

from swagger_server.test import BaseTestCase
from swagger_server.model import db

class TestConsumersController(BaseTestCase):

    def test_search_specimen(self):

        # Specimen ID not in database
        response = self.client.open(
            '/api/v2/specimens/SAN0000100zzzzz',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals([], response.json)

        # Single answer
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

        # Two answers
        response = self.client.open(
            '/api/v2/specimens/SAN0000101',
            method='GET')
        expect = [{
            "specimenId": "SAN0000101",
            "tolIds": [
                {
                    "tolId": "wuAreMari2",
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
                },
                {
                    "tolId": "wpPerVanc1",
                    "species":{
                        "commonName": "None",
                        "family": "Nereididae",
                        "genus": "Perinereis",
                        "kingdom": "Metazoa",
                        "order": "Phyllodocida",
                        "phylum": "Annelida",
                        "prefix": "wpPerVanc",
                        "scientificName": "Perinereis vancaurica",
                        "taxaClass": "Polychaeta",
                        "taxonomyId": 6355
                    }
                }
            ]
        }]
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

        # All data given - another taxon for same specimen
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari2',
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
            "tolId": "wuAreMari2",
            "specimen": {"specimenId": "SAN0000101"}
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)


    def test_search_tol_id_by_taxon_specimen(self):

        # ToLID not in database
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN99999999'}
        response = self.client.open(
            '/api/v2/tol-ids/search',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals([], response.json)

        # All data given
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN0000100'}
        response = self.client.open(
            '/api/v2/tol-ids/search',
            method='GET',
            query_string=query_string)
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
            '/api/v2/tol-ids/search',
            method='GET',
            query_string=query_string)
        self.assertEquals(expect, response.json)

        # All data given - another taxon for same specimen
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN0000101'}
        response = self.client.open(
            '/api/v2/tol-ids/search',
            method='GET',
            query_string=query_string)
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
            "tolId": "wuAreMari2",
            "specimen": {"specimenId": "SAN0000101"}
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
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
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Specimen ID not in database, multiple taxons for same specimen - should create them
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100xxxxx'},
                {'taxonomyId': 6355,
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
            "tolId": "wuAreMari3",
            "specimen": {"specimenId": "SAN0000100xxxxx"},
        },
        {
            "species": {
                "commonName": "None",
                "family": "Nereididae",
                "genus": "Perinereis",
                "kingdom": "Metazoa",
                "order": "Phyllodocida",
                "phylum": "Annelida",
                "prefix": "wpPerVanc",
                "scientificName": "Perinereis vancaurica",
                "taxaClass": "Polychaeta",
                "taxonomyId": 6355
            },
            "tolId": "wpPerVanc2",
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
            'tolId': 'wuAreMari4',
            'specimen': {'specimenId': 'SAN0000100wwwww'},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Search for existing and 2 new
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100ppppp'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100qqqqq'}]
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
            'tolId': 'wuAreMari5',
            'specimen': {'specimenId': 'SAN0000100ppppp'},
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
            'tolId': 'wuAreMari6',
            'specimen': {'specimenId': 'SAN0000100qqqqq'},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Search for existing and new, plus duplicated queries
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100rrrrr'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100rrrrr'}]
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
            'tolId': 'wuAreMari7',   # We created wuAreMari3,4,5,6 earlier on in this method
            'specimen': {'specimenId': 'SAN0000100rrrrr'},
        },
        {
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
            'tolId': 'wuAreMari7',
            'specimen': {'specimenId': 'SAN0000100rrrrr'},
        }]

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Error on later query
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100bbbbb'},
                {'taxonomyId': 9999999,
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

    def test_search_tol_ids_for_user(self):
        self.specimen2.user = self.user2
        db.session.commit()

        # No authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            headers={"api-key": "12345678"},
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Search for user1's ToLIDs
        response = self.client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            headers={"api-key": self.api_key}
            )
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
            "species": {
                "commonName": "None",
                "family": "Nereididae",
                "genus": "Perinereis",
                "kingdom": "Metazoa",
                "order": "Phyllodocida",
                "phylum": "Annelida",
                "prefix": "wpPerVanc",
                "scientificName": "Perinereis vancaurica",
                "taxaClass": "Polychaeta",
                "taxonomyId": 6355
            },
            'tolId': 'wpPerVanc1',
            'specimen': {'specimenId': 'SAN0000101'},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Search for user2's ToLIDs
        response = self.client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            headers={"api-key": self.api_key2}
            )
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
            "specimen": {"specimenId": "SAN0000101"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

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

    def test_add_request(self):
        # No authorisation token given
        query_string = []
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            query_string=query_string)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        query_string = []
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": "12345678"},
            query_string=query_string)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        query_string = []
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        query_string = [('taxonomyId', 6344)]
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database - allowed
        query_string = [('taxonomyId', 999999999),
                         ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        expect = [{
            "species": {
                "taxonomyId": 999999999
            },
            "specimen": {"specimenId": "SAN0000100"},
        }]

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Second taxonomy ID for specimen
        query_string = [('taxonomyId', '6355'),
                        ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        expect = [{
            "species": {
                "commonName": "None",
                "family": "Nereididae",
                "genus": "Perinereis",
                "kingdom": "Metazoa",
                "order": "Phyllodocida",
                "phylum": "Annelida",
                "prefix": "wpPerVanc",
                "scientificName": "Perinereis vancaurica",
                "taxaClass": "Polychaeta",
                "taxonomyId": 6355
            },
            "specimen": {"specimenId": "SAN0000100"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Specimen ID not in database
        query_string = [('taxonomyId', 6344),
                ('specimenId', 'SAN0000100xxxxx')]
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
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
            "specimen": {"specimenId": "SAN0000100xxxxx"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Same again by same user
        query_string = [('taxonomyId', 6344),
                ('specimenId', 'SAN0000100xxxxx')]
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
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
            "specimen": {"specimenId": "SAN0000100xxxxx"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEquals(expect, response.json)

        # Same again by different user
        query_string = [('taxonomyId', 6344),
                ('specimenId', 'SAN0000100xxxxx')]
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key2},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Request for existing ToLID
        query_string = [('taxonomyId', 6344),
                ('specimenId', 'SAN0000100')]
        response = self.client.open(
            '/api/v2/requests',
            method='PUT',
            headers={"api-key": self.api_key},
            query_string=query_string)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))



if __name__ == '__main__':
    import unittest
    unittest.main()
