# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from __future__ import absolute_import

from main.model import TolidPrimaryPrefix, TolidRequest, \
    TolidSecondaryPrefix

from test.system.asserts import assert200, assert400, assert401, assert404, assertEqual


class TestUsersController:

    def test_search_specimen(self, client, data):
        # Specimen ID not in database
        response = client.open(
            '/api/v2/specimens/SAN0000100zzzzz',
            method='GET')
        assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Single answer
        response = client.open(
            '/api/v2/specimens/SAN0000100',
            method='GET')
        expect = [{
            'specimenId': 'SAN0000100',
            'tolIds': [
                {
                    'tolId': 'wuAreMari1',
                    'species': {
                        'commonName': 'lugworm',
                        'currentHighestTolidNumber': 2,
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
                    'user': {'email': data.user_requester.email,
                             'name': data.user_requester.name,
                             'organisation': data.user_requester.organisation,
                             'roles': []}
                }
            ]
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Same again
        response = client.open(
            '/api/v2/specimens/SAN0000100',
            method='GET')
        assertEqual(expect, response.json)

        # Two answers
        response = client.open(
            '/api/v2/specimens/SAN0000101',
            method='GET')
        expect = [{
            'specimenId': 'SAN0000101',
            'tolIds': [
                {
                    'tolId': 'wuAreMari2',
                    'species': {
                        'commonName': 'lugworm',
                        'currentHighestTolidNumber': 2,
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
                    'user': {'email': data.user_requester.email,
                             'name': data.user_requester.name,
                             'organisation': data.user_requester.organisation,
                             'roles': []}
                },
                {
                    'tolId': 'wpPerVanc1',
                    'species': {
                        'commonName': 'None',
                        'currentHighestTolidNumber': 1,
                        'family': 'Nereididae',
                        'genus': 'Perinereis',
                        'kingdom': 'Metazoa',
                        'order': 'Phyllodocida',
                        'phylum': 'Annelida',
                        'prefix': 'wpPerVanc',
                        'scientificName': 'Perinereis vancaurica',
                        'taxaClass': 'Polychaeta',
                        'taxonomyId': 6355
                    },
                    'user': {'email': data.user_requester.email,
                             'name': data.user_requester.name,
                             'organisation': data.user_requester.organisation,
                             'roles': []}

                }
            ]
        }]
        assertEqual(expect, response.json)

    def test_search_tol_id(self, client, data):

        # ToLID not in database
        response = client.open(
            '/api/v2/tol-ids/wuAreMari99999',
            method='GET')
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual([], response.json)

        # All data given
        response = client.open(
            '/api/v2/tol-ids/wuAreMari1',
            method='GET')
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wuAreMari1',
            'specimen': {'specimenId': 'SAN0000100'},
            'user': {'email': data.user_requester.email,
                     'name': data.user_requester.name,
                     'organisation': data.user_requester.organisation,
                     'roles': []}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Same again
        response = client.open(
            '/api/v2/tol-ids/wuAreMari1',
            method='GET')
        assertEqual(expect, response.json)

        # All data given - another taxon for same specimen
        response = client.open(
            '/api/v2/tol-ids/wuAreMari2',
            method='GET')
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wuAreMari2',
            'specimen': {'specimenId': 'SAN0000101'},
            'user': {'email': data.user_requester.email,
                     'name': data.user_requester.name,
                     'organisation': data.user_requester.organisation,
                     'roles': []}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_search_tol_id_by_taxon_specimen(self, client, data):
        # ToLID not in database
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN99999999'}
        response = client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual([], response.json)

        # taxonomyId not an integer
        query_string = {'taxonomyId': 'non-numeric', 'specimenId': 'SAN0000100'}
        response = client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # All data given
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN0000100'}
        response = client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wuAreMari1',
            'specimen': {'specimenId': 'SAN0000100'},
            'user': {'email': data.user_requester.email,
                     'name': data.user_requester.name,
                     'organisation': data.user_requester.organisation,
                     'roles': []}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Same again
        response = client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        assertEqual(expect, response.json)

        # All data given - another taxon for same specimen
        query_string = {'taxonomyId': 6344, 'specimenId': 'SAN0000101'}
        response = client.open(
            '/api/v2/tol-ids',
            method='GET',
            query_string=query_string)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wuAreMari2',
            'specimen': {'specimenId': 'SAN0000101'},
            'user': {'email': data.user_requester.email,
                     'name': data.user_requester.name,
                     'organisation': data.user_requester.organisation,
                     'roles': []}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_search_tol_ids_for_user(self, session, client, data):
        self.specimen2.user = data.user_admin
        session.commit()

        # No authorisation token given
        body = []
        response = client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            headers={'api-key': '12345678'},
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Search for user_requester's ToLIDs
        response = client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            headers={'api-key': data.user_requester.api_key}
        )
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wuAreMari1',
            'specimen': {'specimenId': 'SAN0000100'},
            'user': {'email': data.user_requester.email,
                     'name': data.user_requester.name,
                     'organisation': data.user_requester.organisation,
                     'roles': []}
        }, {
            'species': {
                'commonName': 'None',
                'currentHighestTolidNumber': 1,
                'family': 'Nereididae',
                'genus': 'Perinereis',
                'kingdom': 'Metazoa',
                'order': 'Phyllodocida',
                'phylum': 'Annelida',
                'prefix': 'wpPerVanc',
                'scientificName': 'Perinereis vancaurica',
                'taxaClass': 'Polychaeta',
                'taxonomyId': 6355
            },
            'tolId': 'wpPerVanc1',
            'specimen': {'specimenId': 'SAN0000101'},
            'user': {'email': data.user_requester.email,
                     'name': data.user_requester.name,
                     'organisation': data.user_requester.organisation,
                     'roles': []}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Search for user_admin's ToLIDs
        response = client.open(
            '/api/v2/tol-ids/mine',
            method='GET',
            headers={'api-key': data.user_admin.api_key}
        )
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wuAreMari2',
            'specimen': {'specimenId': 'SAN0000101'},
            'user': {'email': data.user_admin.email,
                     'name': data.user_admin.name,
                     'organisation': data.user_admin.organisation,
                     'roles': [{'role': 'admin'}]}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_search_species(self, client):
        # Taxonomy ID not in database
        response = client.open(
            '/api/v2/species/999999999',
            method='GET')
        assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database and not an integer
        response = client.open(
            '/api/v2/species/abcd',
            method='GET')
        assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # All data given
        response = client.open(
            '/api/v2/species/6344',
            method='GET')
        expect = [{
            'commonName': 'lugworm',
            'currentHighestTolidNumber': 2,
            'family': 'Arenicolidae',
            'genus': 'Arenicola',
            'order': 'None',
            'phylum': 'Annelida',
            'kingdom': 'Metazoa',
            'prefix': 'wuAreMari',
            'scientificName': 'Arenicola marina',
            'taxaClass': 'Polychaeta',
            'taxonomyId': 6344,
            'tolIds': [
                {
                    'specimen': {
                        'specimenId': 'SAN0000100'
                    },
                    'tolId': 'wuAreMari1'
                },
                {
                    'specimen': {
                        'specimenId': 'SAN0000101'
                    },
                    'tolId': 'wuAreMari2'
                }
            ]
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Same again
        response = client.open(
            '/api/v2/species/6344',
            method='GET')
        assertEqual(expect, response.json)

    def search_species_by_taxon_prefix_genus(self, client):
        # Taxonomy ID not in database
        query_string = {'taxonomyId': 999999999}
        response = client.open(
            '/api/v2/species',
            method='GET',
            query_string=query_string)
        expect = []
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Taxonomy ID not in database and not an integer
        query_string = {'taxonomyId': 'abcd'}
        response = client.open(
            '/api/v2/species',
            method='GET',
            query_string=query_string)
        expect = []
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # All data given
        query_string = {'taxonomyId': 6344,
                        'prefix': 'mHomSap',
                        'scientificName': 'Perinereis vancaurica'}
        response = client.open(
            '/api/v2/species',
            method='GET',
            query_string=query_string)
        expect = [{
            'commonName': 'lugworm',
            'currentHighestTolidNumber': 2,
            'family': 'Arenicolidae',
            'genus': 'Arenicola',
            'order': 'None',
            'phylum': 'Annelida',
            'kingdom': 'Metazoa',
            'prefix': 'wuAreMari',
            'scientificName': 'Arenicola marina',
            'taxaClass': 'Polychaeta',
            'taxonomyId': 6344,
            'tolIds': [
                {
                    'specimen': {
                        'specimenId': 'SAN0000100'
                    },
                    'tolId': 'wuAreMari1'
                },
                {
                    'specimen': {
                        'specimenId': 'SAN0000101'
                    },
                    'tolId': 'wuAreMari2'
                }
            ]
        }, {
            'commonName': 'human',
            'currentHighestTolidNumber': 0,
            'family': 'Hominidae',
            'genus': 'Homo',
            'kingdom': 'Metazoa',
            'order': 'Primates',
            'phylum': 'Chordata',
            'prefix': 'mHomSap',
            'scientificName': 'Homo sapiens',
            'taxaClass': 'Mammalia',
            'taxonomyId': 9606,
            'tolIds': []
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # No data given
        response = client.open(
            '/api/v2/species',
            method='GET')
        assertEqual([], response.json)

    def test_search_requests_for_user(self, session, client, data):
        self.request1 = TolidRequest(specimen_id='SAN0000100', species_id=6344, status='Pending')
        self.request1.user = data.user_requester
        session.add(self.request1)
        self.request2 = TolidRequest(specimen_id='SAN0000101', species_id=6344, status='Pending')
        self.request2.user = data.user_requester2
        session.add(self.request2)
        self.request3 = TolidRequest(specimen_id='SAN0000101', species_id=6355, status='Pending')
        self.request3.user = data.user_requester
        session.add(self.request3)
        session.commit()

        # No authorisation token given
        body = []
        response = client.open(
            '/api/v2/requests/mine',
            method='GET',
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = client.open(
            '/api/v2/requests/mine',
            method='GET',
            headers={'api-key': '12345678'},
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Search for user_requester's ToLID requests
        response = client.open(
            '/api/v2/requests/mine',
            method='GET',
            headers={'api-key': data.user_requester.api_key}
        )
        expect = [{
            'reason': None,
            'requestId': 1,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000100'},
        }, {
            'reason': None,
            'requestId': 3,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'None',
                'currentHighestTolidNumber': 1,
                'family': 'Nereididae',
                'genus': 'Perinereis',
                'kingdom': 'Metazoa',
                'order': 'Phyllodocida',
                'phylum': 'Annelida',
                'prefix': 'wpPerVanc',
                'scientificName': 'Perinereis vancaurica',
                'taxaClass': 'Polychaeta',
                'taxonomyId': 6355
            },
            'specimen': {'specimenId': 'SAN0000101'},
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Search for user_requester2's ToLID requests
        response = client.open(
            '/api/v2/requests/mine',
            method='GET',
            headers={'api-key': data.user_requester2.api_key}
        )
        expect = [{
            'reason': None,
            'requestId': 2,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester2',
                'email': 'test_user_requester2@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000101'},
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_bulk_add_requests(self, client, data):
        # No authorisation token given
        body = []
        response = client.open(
            '/api/v2/requests',
            method='POST',
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': '12345678'},
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        body = [{}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        body = [{'taxonomyId': 6344}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        body = [{'taxonomyId': 999999999,
                 'specimenId': 'SAN0000100'}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        expect = [{
            'reason': None,
            'requestId': 1,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'taxonomyId': 999999999
            },
            'specimen': {'specimenId': 'SAN0000100'}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Specimen ID not in database, multiple taxons for same specimen - should create them
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100xxxxx'},
                {'taxonomyId': 6355,
                'specimenId': 'SAN0000100xxxxx'}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        expect = [{
            'reason': None,
            'requestId': 2,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000100xxxxx'},
        }, {
            'reason': None,
            'requestId': 3,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'None',
                'currentHighestTolidNumber': 1,
                'family': 'Nereididae',
                'genus': 'Perinereis',
                'kingdom': 'Metazoa',
                'order': 'Phyllodocida',
                'phylum': 'Annelida',
                'prefix': 'wpPerVanc',
                'scientificName': 'Perinereis vancaurica',
                'taxaClass': 'Polychaeta',
                'taxonomyId': 6355
            },
            'specimen': {'specimenId': 'SAN0000100xxxxx'},
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Existing ToLID
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Existing and new
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100wwwww'}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert400(response,
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
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        expect = [{
            'reason': None,
            'requestId': 4,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000100ggggg'},
        }, {
            'reason': None,
            'requestId': 5,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'reason': None,
            'requestId': 4,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000100ggggg'},
        }, {
            'reason': None,
            'requestId': 5,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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

        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Error on later query
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100bbbbb'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)

        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # And the new one should not have been inserted
        response = client.open(
            '/api/v2/requests/6',
            method='GET')
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual([], response.json)

        # add another request, with confirmation scientific name specified
        confirmation_scientific_name = 'This charming test'
        body = [{'taxonomyId': 6344,
                 'specimenId': 'SAN0000100hahahaha',
                 'confirmationName': confirmation_scientific_name}]
        response = client.open(
            '/api/v2/requests',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        expect = [{
            'reason': None,
            'requestId': 7,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000100hahahaha'},
            'confirmationName': confirmation_scientific_name
        }]
        assertEqual(expect, response.json)

    def test_search_request(self, session, client, data):
        self.request1 = TolidRequest(specimen_id='SAN0000100', species_id=6344, status='Pending')
        self.request1.user = data.user_requester
        session.add(self.request1)
        self.request2 = TolidRequest(specimen_id='SAN0000101', species_id=6344, status='Pending')
        self.request2.user = data.user_requester2
        session.add(self.request2)
        self.request3 = TolidRequest(specimen_id='SAN0000101', species_id=6355, status='Pending')
        self.request3.user = data.user_requester
        session.add(self.request3)
        session.commit()

        # ID not in database
        response = client.open(
            '/api/v2/requests/4',
            method='GET')
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual([], response.json)

        # All data given
        response = client.open(
            '/api/v2/requests/1',
            method='GET')
        expect = [{
            'reason': None,
            'requestId': 1,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000100'}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Same again
        response = client.open(
            '/api/v2/requests/1',
            method='GET')
        assertEqual(expect, response.json)

        # All data given - another taxon for same specimen
        response = client.open(
            '/api/v2/requests/2',
            method='GET')
        expect = [{
            'reason': None,
            'requestId': 2,
            'status': 'Pending',
            'createdBy': {
                'name': 'test_user_requester2',
                'email': 'test_user_requester2@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 2,
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
            'specimen': {'specimenId': 'SAN0000101'}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_retrieve_prefixes(self, session, client):
        self.primary1 = TolidPrimaryPrefix(letter='a',
                                        name='amphibia')
        session.add(self.primary1)
        self.secondary1 = TolidSecondaryPrefix(letter='',
                                            name='Amphibia',
                                            primary_prefix_letter='a')
        session.add(self.secondary1)
        self.primary2 = TolidPrimaryPrefix(letter='c',
                                        name='non-vascular plants')
        session.add(self.primary2)
        self.secondary2 = TolidSecondaryPrefix(letter='a',
                                            name='Andreaeopsida',
                                            primary_prefix_letter='c')
        session.add(self.secondary2)
        session.commit()

        response = client.open(
            '/api/v2/prefix/all',
            method='GET')
        expect = [
            {
                'letter': 'a',
                'name': 'amphibia',
                'secondaryPrefixes': [{
                    'letter': '',
                    'name': 'Amphibia'
                }]
            },
            {
                'letter': 'c',
                'name': 'non-vascular plants',
                'secondaryPrefixes': [{
                    'letter': 'a',
                    'name': 'Andreaeopsida'
                }]
            }
        ]
        assertEqual(expect, response.json)

    def test_list_assigned_tolid_species(self, client):
        response = client.open(
            '/api/v2/species/tol-ids/all/0',
            method='GET')
        expect = [{
            'commonName': 'lugworm',
            'currentHighestTolidNumber': 2,
            'family': 'Arenicolidae',
            'genus': 'Arenicola',
            'order': 'None',
            'phylum': 'Annelida',
            'kingdom': 'Metazoa',
            'prefix': 'wuAreMari',
            'scientificName': 'Arenicola marina',
            'taxaClass': 'Polychaeta',
            'taxonomyId': 6344,
            'tolIds': [
                {
                    'specimen': {
                        'specimenId': 'SAN0000100'
                    },
                    'tolId': 'wuAreMari1'
                },
                {
                    'specimen': {
                        'specimenId': 'SAN0000101'
                    },
                    'tolId': 'wuAreMari2'
                }
            ]
        }, {
            'commonName': 'None',
            'currentHighestTolidNumber': 1,
            'family': 'Nereididae',
            'genus': 'Perinereis',
            'kingdom': 'Metazoa',
            'order': 'Phyllodocida',
            'phylum': 'Annelida',
            'prefix': 'wpPerVanc',
            'scientificName': 'Perinereis vancaurica',
            'taxaClass': 'Polychaeta',
            'taxonomyId': 6355,
            'tolIds': [
                {
                    'specimen': {
                        'specimenId': 'SAN0000101'
                    },
                    'tolId': 'wpPerVanc1'
                }
            ]
        }]
        assertEqual(expect, response.json)

        response = client.open(
            '/api/v2/species/tol-ids/all/5',
            method='GET')
        expect = []
        assertEqual(expect, response.json)


if __name__ == '__main__':
    import unittest
    unittest.main()
