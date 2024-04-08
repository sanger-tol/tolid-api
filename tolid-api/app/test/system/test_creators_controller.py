# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from __future__ import absolute_import

from test.system.asserts import assert200, assert400, assert401, assert403, assertEqual


class TestCreatorsController:

    def test_add_tolid(self, client, data):
        # No authorisation token given
        query_string = []
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            query_string=query_string)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        query_string = []
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': '12345678'},
            query_string=query_string)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        query_string = []
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_creator.api_key},
            query_string=query_string)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        query_string = [('taxonomyId', 6344)]
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_creator.api_key},
            query_string=query_string)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        query_string = [('taxonomyId', 999999999),
                        ('specimenId', 'SAN0000100')]
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_creator.api_key},
            query_string=query_string)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # User not a creator
        query_string = [('taxonomyId', '6355'),
                        ('specimenId', 'SAN0000100')]
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_requester.api_key},
            query_string=query_string)
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Second taxonomy ID for specimen
        query_string = [('taxonomyId', '6355'),
                        ('specimenId', 'SAN0000100')]
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_creator.api_key},
            query_string=query_string)
        expect = [{
            'species': {
                'commonName': 'None',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wpPerVanc2',
            'specimen': {'specimenId': 'SAN0000100'},
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Specimen ID not in database - should create it
        query_string = [('taxonomyId', 6344),
                        ('specimenId', 'SAN0000100xxxxx')]
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_creator.api_key},
            query_string=query_string)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 3,
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
            'specimen': {'specimenId': 'SAN0000100xxxxx'},
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Specimen ID not in database and first for species - should create it
        query_string = [('taxonomyId', 9606),
                        ('specimenId', 'SAN0000999xxxxx')]
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_creator.api_key},
            query_string=query_string)
        expect = [{
            'species': {
                'commonName': 'human',
                'currentHighestTolidNumber': 1,
                'family': 'Hominidae',
                'genus': 'Homo',
                'order': 'Primates',
                'phylum': 'Chordata',
                'kingdom': 'Metazoa',
                'prefix': 'mHomSap',
                'scientificName': 'Homo sapiens',
                'taxaClass': 'Mammalia',
                'taxonomyId': 9606
            },
            'tolId': 'mHomSap1',
            'specimen': {'specimenId': 'SAN0000999xxxxx'},
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Existing - should return existing
        query_string = [('taxonomyId', 6344),
                        ('specimenId', 'SAN0000100')]
        response = client.open(
            '/api/v2/tol-ids',
            method='PUT',
            headers={'api-key': data.user_creator.api_key},
            query_string=query_string)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 3,
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

    def test_bulk_search_tol_ids(self, client, data):
        # No authorisation token given
        body = []
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': '12345678'},
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No taxonomyId given
        body = [{}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # No specimenId given
        body = [{'taxonomyId': 6344}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database - should get a request back
        body = [{'taxonomyId': 999999999,
                 'specimenId': 'SAN0000100'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        expect = [{'createdBy': {'email': 'test_user_creator@sanger.ac.uk',
                                 'name': 'test_user_creator',
                                 'organisation': 'Sanger Institute',
                                 'roles': [{'role': 'creator'}]},
                   'reason': None,
                   'requestId': 1,
                   'species': {'taxonomyId': 999999999},
                   'specimen': {'specimenId': 'SAN0000100'},
                   'status': 'Pending'}]
        assertEqual(expect, response.json)

        # User doesn't have creator role
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Specimen ID not in database, multiple taxons for same specimen - should create them
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100xxxxx'},
                {'taxonomyId': 6355,
                'specimenId': 'SAN0000100xxxxx'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 3,
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
            'specimen': {'specimenId': 'SAN0000100xxxxx'},
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }, {
            'species': {
                'commonName': 'None',
                'currentHighestTolidNumber': 2,
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
            'tolId': 'wpPerVanc2',
            'specimen': {'specimenId': 'SAN0000100xxxxx'},
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Single search for existing
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 3,
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

        # Search for existing and new
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100wwwww'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 4,
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
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 4,
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
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Search for existing and 2 new
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100ppppp'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100qqqqq'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 6,
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
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 6,
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
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }, {
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 6,
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
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Search for existing and new, plus duplicated queries
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100rrrrr'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100'},
                {'taxonomyId': 6344,
                'specimenId': 'SAN0000100rrrrr'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 7,
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
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 7,
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
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }, {
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 7,
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
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 7,
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
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }]

        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Later query returns a request
        body = [{'taxonomyId': 6344,
                'specimenId': 'SAN0000100bbbbb'},
                {'taxonomyId': 9999999,
                'specimenId': 'SAN0000100'}]
        response = client.open(
            '/api/v2/tol-ids',
            method='POST',
            headers={'api-key': data.user_creator.api_key},
            json=body)

        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        expect = [{
            'species': {
                'commonName': 'lugworm',
                'currentHighestTolidNumber': 8,
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
            'tolId': 'wuAreMari8',
            'specimen': {'specimenId': 'SAN0000100bbbbb'},
            'user': {'email': data.user_creator.email,
                     'name': data.user_creator.name,
                     'organisation': data.user_creator.organisation,
                     'roles': [{'role': 'creator'}]}
        }, {
            'createdBy': {'email': 'test_user_creator@sanger.ac.uk',
                          'name': 'test_user_creator',
                          'organisation': 'Sanger Institute',
                          'roles': [{'role': 'creator'}]},
            'reason': None,
            'requestId': 2,
            'species': {'taxonomyId': 9999999},
            'specimen': {'specimenId': 'SAN0000100'},
            'status': 'Pending'}]
        assertEqual(expect, response.json)

        # And the new one should have been inserted
        response = client.open(
            '/api/v2/specimens/SAN0000100bbbbb',
            method='GET')
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        expect = [{
            'specimenId': 'SAN0000100bbbbb',
            'tolIds': [
                {'species': {'commonName': 'lugworm',
                             'currentHighestTolidNumber': 8,
                             'family': 'Arenicolidae',
                             'genus': 'Arenicola',
                             'order': 'None',
                             'phylum': 'Annelida',
                             'kingdom': 'Metazoa',
                             'prefix': 'wuAreMari',
                             'scientificName': 'Arenicola marina',
                             'taxaClass': 'Polychaeta',
                             'taxonomyId': 6344},
                 'tolId': 'wuAreMari8',
                 'user': {'email': data.user_creator.email,
                          'name': data.user_creator.name,
                          'organisation': data.user_creator.organisation,
                          'roles': [{'role': 'creator'}]}}
            ]
        }]
        assertEqual(expect, response.json)

        response = client.open(
            '/api/v2/requests/2',
            method='GET')
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        expect = [{'createdBy': {'email': 'test_user_creator@sanger.ac.uk',
                                 'name': 'test_user_creator',
                                 'organisation': 'Sanger Institute',
                                 'roles': [{'role': 'creator'}]},
                   'reason': None,
                   'requestId': 2,
                   'species': {'taxonomyId': 9999999},
                   'specimen': {'specimenId': 'SAN0000100'},
                   'status': 'Pending'}]
        assertEqual(expect, response.json)
