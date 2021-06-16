from __future__ import absolute_import

from swagger_server.test import BaseTestCase
from swagger_server.model import db, TolidRequest


class TestUsersController(BaseTestCase):

    def test_search_specimen(self):
        # Specimen ID not in database
        response = self.client.open(
            '/api/v2/specimens/SAN0000100zzzzz',
            method='GET')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Single answer
        response = self.client.open(
            '/api/v2/specimens/SAN0000100',
            method='GET')
        expect = [{
            "specimenId": "SAN0000100",
            "tolIds": [
                {
                    "tolId": "wuAreMari1",
                    "species": {
                        "commonName": "lugworm",
                        "currentHighestTolidNumber": 2,
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
        self.assertEqual(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/specimens/SAN0000100',
            method='GET')
        self.assertEqual(expect, response.json)

        # Two answers
        response = self.client.open(
            '/api/v2/specimens/SAN0000101',
            method='GET')
        expect = [{
            "specimenId": "SAN0000101",
            "tolIds": [
                {
                    "tolId": "wuAreMari2",
                    "species": {
                        "commonName": "lugworm",
                        "currentHighestTolidNumber": 2,
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
                    "species": {
                        "commonName": "None",
                        "currentHighestTolidNumber": 1,
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
        self.assertEqual(expect, response.json)

    def test_search_tol_id(self):

        # ToLID not in database
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari99999',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual([], response.json)

        # All data given
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari1',
            method='GET')
        expect = [{
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
        self.assertEqual(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari1',
            method='GET')
        self.assertEqual(expect, response.json)

        # All data given - another taxon for same specimen
        response = self.client.open(
            '/api/v2/tol-ids/wuAreMari2',
            method='GET')
        expect = [{
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
        self.assertEqual(expect, response.json)

    def test_search_tol_id_by_taxon_specimen(self):
        # ToLID not in database
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN99999999'}
        response = self.client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual([], response.json)

        # taxonomyId not an integer
        query_string = {'taxonomyId': 'non-numeric', 'specimenId': 'SAN0000100'}
        response = self.client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # All data given
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN0000100'}
        response = self.client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        expect = [{
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
        self.assertEqual(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        self.assertEqual(expect, response.json)

        # All data given - another taxon for same specimen
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN0000101'}
        response = self.client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        expect = [{
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
        self.assertEqual(expect, response.json)

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
            headers={"api-key": self.user1.api_key}
            )
        expect = [{
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
        }, {
            "species": {
                "commonName": "None",
                "currentHighestTolidNumber": 1,
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
        self.assertEqual(expect, response.json)

        # Search for user2's ToLIDs
        response = self.client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            headers={"api-key": self.user2.api_key}
            )
        expect = [{
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
        self.assertEqual(expect, response.json)

    def test_search_species(self):
        # Taxonomy ID not in database
        response = self.client.open(
            '/api/v2/species/999999999',
            method='GET')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database and not an integer
        response = self.client.open(
            '/api/v2/species/abcd',
            method='GET')
        self.assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # All data given
        response = self.client.open(
            '/api/v2/species/6344',
            method='GET')
        expect = [{
            "commonName": "lugworm",
            "currentHighestTolidNumber": 2,
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "kingdom": "Metazoa",
            "prefix": "wuAreMari",
            "scientificName": "Arenicola marina",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6344,
            "tolIds": [
                {
                    "specimen": {
                        "specimenId": "SAN0000100"
                    },
                    "tolId": "wuAreMari1"
                },
                {
                    "specimen": {
                        "specimenId": "SAN0000101"
                    },
                    "tolId": "wuAreMari2"
                }
            ]
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/species/6344',
            method='GET')
        self.assertEqual(expect, response.json)

    def test_search_species_by_taxon_prefix_name(self):
        # Taxonomy ID not in database
        query_string = {'taxonomyId': 999999999}
        response = self.client.open(
            '/api/v2/species',
            method='GET',
            query_string=query_string)
        expect = []
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # Taxonomy ID not in database and not an integer
        query_string = {'taxonomyId': 'abcd'}
        response = self.client.open(
            '/api/v2/species',
            method='GET',
            query_string=query_string)
        expect = []
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # All data given
        query_string = {'taxonomyId': 6344,
                        'prefix': 'mHomSap',
                        'scientificName': 'Perinereis vancaurica'}
        response = self.client.open(
            '/api/v2/species',
            method='GET',
            query_string=query_string)
        expect = [{
            "commonName": "lugworm",
            "currentHighestTolidNumber": 2,
            "family": "Arenicolidae",
            "genus": "Arenicola",
            "order": "None",
            "phylum": "Annelida",
            "kingdom": "Metazoa",
            "prefix": "wuAreMari",
            "scientificName": "Arenicola marina",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6344,
            "tolIds": [
                {
                    "specimen": {
                        "specimenId": "SAN0000100"
                    },
                    "tolId": "wuAreMari1"
                },
                {
                    "specimen": {
                        "specimenId": "SAN0000101"
                    },
                    "tolId": "wuAreMari2"
                }
            ]
        }, {
            "commonName": "None",
            "currentHighestTolidNumber": 1,
            "family": "Nereididae",
            "genus": "Perinereis",
            "kingdom": "Metazoa",
            "order": "Phyllodocida",
            "phylum": "Annelida",
            "prefix": "wpPerVanc",
            "scientificName": "Perinereis vancaurica",
            "taxaClass": "Polychaeta",
            "taxonomyId": 6355,
            "tolIds": [
                {
                    "specimen": {
                        "specimenId": "SAN0000101"
                    },
                    "tolId": "wpPerVanc1"
                }
            ]
        }, {
            "commonName": "human",
            "currentHighestTolidNumber": 0,
            "family": "Hominidae",
            "genus": "Homo",
            "kingdom": "Metazoa",
            "order": "Primates",
            "phylum": "Chordata",
            "prefix": "mHomSap",
            "scientificName": "Homo sapiens",
            "taxaClass": "Mammalia",
            "taxonomyId": 9606,
            "tolIds": []
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # No data given
        response = self.client.open(
            '/api/v2/species',
            method='GET')
        self.assertEqual([], response.json)

    def test_search_requests_for_user(self):
        self.request1 = TolidRequest(specimen_id="SAN0000100", species_id=6344, status="Pending")
        self.request1.user = self.user1
        db.session.add(self.request1)
        self.request2 = TolidRequest(specimen_id="SAN0000101", species_id=6344, status="Pending")
        self.request2.user = self.user4
        db.session.add(self.request2)
        self.request3 = TolidRequest(specimen_id="SAN0000101", species_id=6355, status="Pending")
        self.request3.user = self.user1
        db.session.add(self.request3)
        db.session.commit()

        # No authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/requests/mine',
            method='GET',
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/requests/mine',
            method='GET',
            headers={"api-key": "12345678"},
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Search for user1's ToLID requests
        response = self.client.open(
            '/api/v2/requests/mine',
            method='GET',
            headers={"api-key": self.user1.api_key}
            )
        expect = [{
            "requestId": 1,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
            "specimen": {"specimenId": "SAN0000100"},
        }, {
            "requestId": 3,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "None",
                "currentHighestTolidNumber": 1,
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
            'specimen': {'specimenId': 'SAN0000101'},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # Search for user4's ToLID requests
        response = self.client.open(
            '/api/v2/requests/mine',
            method='GET',
            headers={"api-key": self.user4.api_key}
            )
        expect = [{
            "requestId": 2,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester2",
                "email": "test_user_requester2@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
            "specimen": {"specimenId": "SAN0000101"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

    def test_bulk_add_requests(self):
        # No authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": "12345678"},
            json=body)
        self.assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        body = [{}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        body = [{'taxonomyId': 6344}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        body = [{'taxonomyId': 999999999,
                 'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)
        expect = [{
            "requestId": 1,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "taxonomyId": 999999999
            },
            "specimen": {"specimenId": "SAN0000100"}
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # Specimen ID not in database, multiple taxons for same specimen - should create them
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100xxxxx'},
                {'taxonomyId': 6355,
                'specimenId': 'SAN0000100xxxxx'}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)
        expect = [{
            "requestId": 2,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
        }, {
            "requestId": 3,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "None",
                "currentHighestTolidNumber": 1,
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
            "specimen": {"specimenId": "SAN0000100xxxxx"},
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # Existing ToLID
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Existing and new
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100wwwww'}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Search for 2 new, plus duplicated queries
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100ggggg'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100rrrrr'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100ggggg'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100rrrrr'}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)
        expect = [{
            "requestId": 4,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
            "specimen": {"specimenId": "SAN0000100ggggg"},
        }, {
            "requestId": 5,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            'species': {
                'commonName': 'lugworm',
                "currentHighestTolidNumber": 2,
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
            'specimen': {'specimenId': 'SAN0000100rrrrr'},
        }, {
            "requestId": 4,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
            "specimen": {"specimenId": "SAN0000100ggggg"},
        }, {
            "requestId": 5,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            'species': {
                'commonName': 'lugworm',
                "currentHighestTolidNumber": 2,
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
            'specimen': {'specimenId': 'SAN0000100rrrrr'},
        }]

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # Error on later query
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100bbbbb'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = self.client.open(
            '/api/v2/requests',
            method='POST',
            headers={"api-key": self.user1.api_key},
            json=body)

        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # And the new one should not have been inserted
        response = self.client.open(
            '/api/v2/requests/6',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual([], response.json)

    def test_search_request(self):
        self.request1 = TolidRequest(specimen_id="SAN0000100", species_id=6344, status="Pending")
        self.request1.user = self.user1
        db.session.add(self.request1)
        self.request2 = TolidRequest(specimen_id="SAN0000101", species_id=6344, status="Pending")
        self.request2.user = self.user4
        db.session.add(self.request2)
        self.request3 = TolidRequest(specimen_id="SAN0000101", species_id=6355, status="Pending")
        self.request3.user = self.user1
        db.session.add(self.request3)
        db.session.commit()

        # ID not in database
        response = self.client.open(
            '/api/v2/requests/4',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual([], response.json)

        # All data given
        response = self.client.open(
            '/api/v2/requests/1',
            method='GET')
        expect = [{
            "requestId": 1,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester",
                "email": "test_user_requester@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
            "specimen": {"specimenId": "SAN0000100"}
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)

        # Same again
        response = self.client.open(
            '/api/v2/requests/1',
            method='GET')
        self.assertEqual(expect, response.json)

        # All data given - another taxon for same specimen
        response = self.client.open(
            '/api/v2/requests/2',
            method='GET')
        expect = [{
            "requestId": 2,
            "status": "Pending",
            "createdBy": {
                "name": "test_user_requester2",
                "email": "test_user_requester2@sanger.ac.uk",
                "organisation": "Sanger Institute",
                "roles": []
            },
            "species": {
                "commonName": "lugworm",
                "currentHighestTolidNumber": 2,
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
            "specimen": {"specimenId": "SAN0000101"}
        }]
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertEqual(expect, response.json)


if __name__ == '__main__':
    import unittest
    unittest.main()
