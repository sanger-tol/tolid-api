# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from unittest.mock import patch

from main.model import TolidRequest, TolidSpecimen

from test.system.asserts import assert200, assert400, assert401, assert403, assert404, assertEqual


class TestCuratorsController:

    def test_add_species(self, client, data):
        # No authorisation token given
        query_string = []
        response = client.open(
            '/api/v2/species',
            method='POST',
            query_string=query_string)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        query_string = []
        response = client.open(
            '/api/v2/species',
            method='POST',
            headers={'api-key': '12345678'},
            query_string=query_string)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Not admin
        body = {'taxonomyId': 999999,
                'scientificName': 'Species',
                'prefix': 'whatever',
                'commonName': 'Common name',
                'genus': 'Genus',
                'family': 'Family',
                'order': 'Order',
                'taxaClass': 'Class',
                'phylum': 'Phylum',
                'kingdom': 'Kingdom'}
        response = client.open(
            '/api/v2/species',
            method='POST',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID already in database
        body = {'taxonomyId': 6344,
                'scientificName': 'Species',
                'prefix': 'whatever',
                'commonName': 'Common name',
                'genus': 'Genus',
                'family': 'Family',
                'order': 'Order',
                'taxaClass': 'Class',
                'phylum': 'Phylum',
                'kingdom': 'Kingdom'}
        response = client.open(
            '/api/v2/species',
            method='POST',
            headers={'api-key': data.user_admin.api_key},
            json=body)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database - should create it
        body = {'taxonomyId': 999999,
                'scientificName': 'Species',
                'prefix': 'whatever',
                'commonName': 'Common name',
                'genus': 'Genus',
                'family': 'Family',
                'order': 'Order',
                'taxaClass': 'Class',
                'phylum': 'Phylum',
                'kingdom': 'Kingdom'}
        response = client.open(
            '/api/v2/species',
            method='POST',
            headers={'api-key': data.user_admin.api_key},
            json=body)
        expect = [{
            'commonName': 'Common name',
            'currentHighestTolidNumber': 0,
            'family': 'Family',
            'genus': 'Genus',
            'order': 'Order',
            'phylum': 'Phylum',
            'kingdom': 'Kingdom',
            'prefix': 'whatever',
            'scientificName': 'Species',
            'taxaClass': 'Class',
            'taxonomyId': 999999,
            'tolIds': []
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Has it been added?
        response = client.open(
            '/api/v2/species/999999',
            method='GET')
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_edit_species(self, client, data):
        # No authorisation token given
        query_string = []
        response = client.open(
            '/api/v2/species/6344',
            method='PUT',
            query_string=query_string)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        query_string = []
        response = client.open(
            '/api/v2/species/6344',
            method='PUT',
            headers={'api-key': '12345678'},
            query_string=query_string)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Not admin
        body = {'taxonomyId': 6344,
                'scientificName': 'Species',
                'prefix': 'whatever',
                'commonName': 'Common name',
                'genus': 'Genus',
                'family': 'Family',
                'order': 'Order',
                'taxaClass': 'Class',
                'phylum': 'Phylum',
                'kingdom': 'Kingdom'}
        response = client.open(
            '/api/v2/species/6344',
            method='PUT',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        body = {'taxonomyId': 999999,
                'scientificName': 'Species',
                'prefix': 'whatever',
                'commonName': 'Common name',
                'genus': 'Genus',
                'family': 'Family',
                'order': 'Order',
                'taxaClass': 'Class',
                'phylum': 'Phylum',
                'kingdom': 'Kingdom'}
        response = client.open(
            '/api/v2/species/999999',
            method='PUT',
            headers={'api-key': data.user_admin.api_key},
            json=body)
        assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID not in database
        body = {'taxonomyId': 999999,
                'scientificName': 'Species',
                'prefix': 'whatever',
                'commonName': 'Common name',
                'genus': 'Genus',
                'family': 'Family',
                'order': 'Order',
                'taxaClass': 'Class',
                'phylum': 'Phylum',
                'kingdom': 'Kingdom'}
        response = client.open(
            '/api/v2/species/abcd',
            method='PUT',
            headers={'api-key': data.user_admin.api_key},
            json=body)
        assert404(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID in database - should edit it
        body = {'taxonomyId': 63446344,
                'scientificName': 'Species',
                'prefix': 'whatever',
                'commonName': 'Common name',
                'genus': 'Genus',
                'family': 'Family',
                'order': 'Order',
                'taxaClass': 'Class',
                'phylum': 'Phylum',
                'kingdom': 'Kingdom'}
        response = client.open(
            '/api/v2/species/6344',
            method='PUT',
            headers={'api-key': data.user_admin.api_key},
            json=body)
        expect = [{
            'commonName': 'Common name',
            'currentHighestTolidNumber': 2,
            'family': 'Family',
            'genus': 'Genus',
            'order': 'Order',
            'phylum': 'Phylum',
            'kingdom': 'Kingdom',
            'prefix': 'whatever',
            'scientificName': 'Species',
            'taxaClass': 'Class',
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

        # Has it changed?
        response = client.open(
            '/api/v2/species/6344',
            method='GET')
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_list_specimens(self, session, client, data):
        # Add a couple more specimens
        specimen2 = TolidSpecimen(specimen_id='SAN0000102', number=3, tolid='wuAreMari3')
        specimen2.species = self.species1
        specimen2.user = data.user_requester
        specimen3 = TolidSpecimen(specimen_id='SAN0000103', number=1, tolid='mHomSap1')
        specimen3.species = self.species2
        specimen3.user = data.user_requester

        session.add(specimen2)
        session.add(specimen3)
        session.commit()

        # No authorisation token given
        response = client.open(
            '/api/v2/tol-ids/all',
            method='GET',
        )
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        response = client.open(
            '/api/v2/tol-ids/all',
            method='GET',
            headers={'api-key': '12345678'},
        )
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Not admin
        response = client.open(
            '/api/v2/tol-ids/all',
            method='GET',
            headers={'api-key': data.user_requester.api_key},
        )
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # No taxonomyId given
        query_string = []
        response = client.open(
            '/api/v2/tol-ids/all',
            method='GET',
            headers={'api-key': data.user_admin.api_key},
            query_string=query_string)
        expect = 'wuAreMari1\tArenicola marina\tSAN0000100\t1\nwuAreMari2\tArenicola marina\t' \
            + 'SAN0000101\t2\nwuAreMari3\tArenicola marina\tSAN0000102\t3\nwpPerVanc1\t' \
            + 'Perinereis vancaurica\tSAN0000101\t1\nmHomSap1\tHomo sapiens\tSAN0000103\t1'
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual('text/plain; charset=utf-8', response.content_type)
        assertEqual(expect, response.data.decode('utf-8'))

        # Taxonomy ID not in database
        query_string = [('taxonomyId', '999999999')]
        response = client.open(
            '/api/v2/tol-ids/all',
            method='GET',
            headers={'api-key': data.user_admin.api_key},
            query_string=query_string)
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Taxonomy ID given
        query_string = [('taxonomyId', '6344')]
        response = client.open(
            '/api/v2/tol-ids/all',
            method='GET',
            headers={'api-key': data.user_admin.api_key},
            query_string=query_string)
        expect = 'wuAreMari1\tArenicola marina\tSAN0000100\t1\nwuAreMari2\tArenicola marina\t' \
            + 'SAN0000101\t2\nwuAreMari3\tArenicola marina\tSAN0000102\t3'
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual('text/plain; charset=utf-8', response.content_type)
        assertEqual(expect, response.data.decode('utf-8'))

    def test_list_species(self, client, data):
        # No authorisation token given
        response = client.open(
            '/api/v2/species/all',
            method='GET',
            headers={'accept': 'text/plain'},
        )
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        response = client.open(
            '/api/v2/species/all',
            method='GET',
            headers={'api-key': '12345678', 'accept': 'text/plain'},
        )
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Not admin
        response = client.open(
            '/api/v2/species/all',
            method='GET',
            headers={'api-key': data.user_requester.api_key, 'accept': 'text/plain'},
        )
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # All correct - text/plain
        query_string = []
        response = client.open(
            '/api/v2/species/all',
            method='GET',
            headers={'api-key': data.user_admin.api_key, 'accept': 'text/plain'},
            query_string=query_string)
        expect = 'wuAreMari\tArenicola marina\t6344\tlugworm\tArenicola\tArenicolidae\tNone\t' \
            + 'Polychaeta\tAnnelida\nwpPerVanc\tPerinereis vancaurica\t6355\tNone\tPerinereis\t' \
            + 'Nereididae\tPhyllodocida\tPolychaeta\tAnnelida\nmHomSap\tHomo sapiens\t9606\t' \
            + 'human\tHomo\tHominidae\tPrimates\tMammalia\tChordata'
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual('text/plain; charset=utf-8', response.content_type)
        assertEqual(expect, response.data.decode('utf-8'))

        # All correct - application/json
        query_string = []
        response = client.open(
            '/api/v2/species/all',
            method='GET',
            headers={'api-key': data.user_admin.api_key, 'accept': 'application/json'},
            query_string=query_string)
        expect = [{
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
        }, {
            'commonName': 'None',
            'family': 'Nereididae',
            'genus': 'Perinereis',
            'kingdom': 'Metazoa',
            'order': 'Phyllodocida',
            'phylum': 'Annelida',
            'prefix': 'wpPerVanc',
            'scientificName': 'Perinereis vancaurica',
            'taxaClass': 'Polychaeta',
            'taxonomyId': 6355
        }, {
            'commonName': 'human',
            'family': 'Hominidae',
            'genus': 'Homo',
            'kingdom': 'Metazoa',
            'order': 'Primates',
            'phylum': 'Chordata',
            'prefix': 'mHomSap',
            'scientificName': 'Homo sapiens',
            'taxaClass': 'Mammalia',
            'taxonomyId': 9606
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual('application/json', response.content_type)
        assertEqual(expect, response.json)

    def test_search_pending_requests(self, session, client, data):
        request1 = TolidRequest(specimen_id='SAN0000100', species_id=6344, status='Pending')
        request1.user = data.user_requester
        session.add(request1)
        request2 = TolidRequest(specimen_id='SAN0000101', species_id=6344, status='Pending')
        request2.user = data.user_requester2
        session.add(request2)
        request3 = TolidRequest(specimen_id='SAN0000101', species_id=6355, status='Rejected')
        request3.user = data.user_requester
        session.add(request3)
        session.commit()

        # No authorisation token given
        body = []
        response = client.open(
            '/api/v2/requests/pending',
            method='GET',
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        body = []
        response = client.open(
            '/api/v2/requests/pending',
            method='GET',
            headers={'api-key': '12345678'},
            json=body)
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Not admin
        body = []
        response = client.open(
            '/api/v2/requests/pending',
            method='GET',
            headers={'api-key': data.user_requester.api_key},
            json=body)
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Search for pending ToLID requests
        response = client.open(
            '/api/v2/requests/pending',
            method='GET',
            headers={'api-key': data.user_admin.api_key}
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

    def test_accept_request(self, session, client, data):
        request1 = TolidRequest(specimen_id='SAN0000100', species_id=999999, status='Pending')
        request1.user = data.user_requester
        session.add(request1)
        request2 = TolidRequest(specimen_id='SAN0000101', species_id=6344, status='Pending')
        request2.user = data.user_requester2
        session.add(request2)
        session.commit()

        # No authorisation token given
        response = client.open(
            '/api/v2/requests/1/accept',
            method='PATCH')
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        response = client.open(
            '/api/v2/requests/1/accept',
            method='PATCH',
            headers={'api-key': '12345678'})
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Not admin
        response = client.open(
            '/api/v2/requests/1/accept',
            method='PATCH',
            headers={'api-key': data.user_requester.api_key})
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Invalid species
        response = client.open(
            '/api/v2/requests/1/accept',
            method='PATCH',
            headers={'api-key': data.user_admin.api_key}
        )
        assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Correct
        response = client.open(
            '/api/v2/requests/2/accept',
            method='PATCH',
            headers={'api-key': data.user_admin.api_key}
        )
        expect = [{
            'tolId': 'wuAreMari3',
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
            'specimen': {'specimenId': 'SAN0000101'},
            'user': {'email': data.user_requester2.email,
                     'name': data.user_requester2.name,
                     'organisation': data.user_requester2.organisation,
                     'roles': []}
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

    def test_reject_request(self, session, client, data):
        request1 = TolidRequest(specimen_id='SAN0000100', species_id=999999, status='Pending')
        request1.user = data.user_requester
        session.add(request1)
        request2 = TolidRequest(specimen_id='SAN0000101', species_id=6344, status='Pending')
        request2.user = data.user_requester2
        session.add(request2)
        session.commit()

        # No authorisation token given
        response = client.open(
            '/api/v2/requests/1/reject',
            method='PATCH')
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        response = client.open(
            '/api/v2/requests/1/reject',
            method='PATCH',
            headers={'api-key': '12345678'})
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Not admin
        response = client.open(
            '/api/v2/requests/1/reject',
            method='PATCH',
            headers={'api-key': data.user_requester.api_key})
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Invalid species
        response = client.open(
            '/api/v2/requests/1/reject',
            method='PATCH',
            headers={'api-key': data.user_admin.api_key}
        )
        expect = [{
            'reason': None,
            'requestId': 1,
            'status': 'Rejected',
            'createdBy': {
                'name': 'test_user_requester',
                'email': 'test_user_requester@sanger.ac.uk',
                'organisation': 'Sanger Institute',
                'roles': []
            },
            'species': {
                'taxonomyId': 999999
            },
            'specimen': {'specimenId': 'SAN0000100'},
        }]
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        assertEqual(expect, response.json)

        # Valid species
        response = client.open(
            '/api/v2/requests/2/reject?reason=Taxonomy+ID+is+not+species-level',
            method='PATCH',
            headers={'api-key': data.user_admin.api_key}
        )
        expect = [{
            'reason': 'Taxonomy ID is not species-level',
            'requestId': 2,
            'status': 'Rejected',
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

    @patch('Bio.Entrez.efetch')
    @patch('Bio.Entrez.read')
    def test_get_ncbi_data(self, read, efetch, client, data):
        # No authorisation token given
        response = client.open(
            '/api/v2/species/270330/ncbi',
            method='GET')
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        # Invalid authorisation token given
        response = client.open(
            '/api/v2/species/270330/ncbi',
            method='GET',
            headers={'api-key': '12345678'})
        assert401(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Not admin
        response = client.open(
            '/api/v2/species/270330/ncbi',
            method='GET',
            headers={'api-key': data.user_requester.api_key})
        assert403(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Admin, correct
        mock_ncbi_data = [{
            'ScientificName': 'Lepomis megalotis',
            'OtherNames': {
                'Synonym': [
                    'syn1',
                ],
                'GenbankSynonym': [
                    'syn2',
                ],
            },
        }]
        efetch.return_value = None
        read.return_value = mock_ncbi_data
        response = client.open(
            '/api/v2/species/270330/ncbi',
            method='GET',
            headers={'api-key': data.user_admin.api_key})
        assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        expected = {
            'scientificName': 'Lepomis megalotis',
            'synonyms': [
                'syn1',
                'syn2'
            ]
        }
        assertEqual(expected, response.json)


if __name__ == '__main__':
    import unittest
    unittest.main()
