# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from tol.core import DataSourceFilter


def test_request_user(client, api_path, sql_datasource):
    # Make sure the user does not have "Creator" role
    f = DataSourceFilter()
    f.and_ = {
        'user.id': {'eq': {'value': '100'}},
        'role.name': {'eq': {'value': 'creator'}}
    }
    for rb in sql_datasource.get_list('role_binding', f):
        sql_datasource.delete('role_binding', [rb.id])

    body = [
        {
            'species_id': 1234,
            'specimen_id': 'SPECIMEN1'  # New
        },
        {
            'species_id': 1234,
            'specimen_id': 'SPECIMEN2',  # New, with requested_taxonomy_id
            'requested_taxonomy_id': 5678
        },
        {
            'species_id': 1235,
            'specimen_id': 'SPECIMEN3',  # Species doesn't exist
            'requested_taxonomy_id': 6789
        },
        {
            'species_id': 1234,
            'specimen_id': 'TEST_SPECIMEN1'  # ToLID already exists
        },
        {
            'species_id': 1235,
            'specimen_id': 'TEST_SPECIMEN2'  # Request already exists
        }
    ]
    response = client.post(api_path + '/request/create', json=body)
    assert response.status_code == 400

    errors = response.json['errors']
    assert len(errors) == 2


    obj1 = response.json['data'][0]
    assert obj1['type'] == 'request'
    assert obj1['attributes']['species_id'] == 1234
    assert obj1['attributes']['specimen_id'] == 'SPECIMEN1'
    assert obj1['attributes']['requested_taxonomy_id'] == 1234
    assert obj1['attributes']['status'] == 'Pending'
    assert obj1['relationships']['user']['data']['id'] == '100'

    obj2 = response.json['data'][1]
    assert obj1['type'] == 'request'
    assert obj1['attributes']['species_id'] == 1234
    assert obj1['attributes']['specimen_id'] == 'SPECIMEN2'
    assert obj1['attributes']['requested_taxonomy_id'] == 5678
    assert obj1['attributes']['status'] == 'Pending'
    assert obj1['relationships']['user']['data']['id'] == '100'

    obj3 = response.json['data'][2]
    assert obj3['type'] == 'request'
    assert obj3['attributes']['species_id'] == 1235
    assert obj3['attributes']['specimen_id'] == 'SPECIMEN3'
    assert obj3['attributes']['requested_taxonomy_id'] == 6789
    assert obj3['attributes']['status'] == 'Pending'
    assert obj3['relationships']['user']['data']['id'] == '100'

    obj4 = response.json['data'][3]
    assert obj4['type'] == 'specimen'
    assert obj4['id'] == 'abCdeFghi1'
    assert obj4['attributes']['number'] == 1
    assert obj4['attributes']['specimen_id'] == 'TEST_SPECIMEN1'
    assert obj2['relationships']['species']['data']['id'] == '1234'
    assert obj4['relationships']['user']['data']['id'] == '200'

    obj5 = response.json['data'][4]
    assert obj5['type'] == 'request'
    assert obj5['attributes']['species_id'] == 1235
    assert obj5['attributes']['specimen_id'] == 'TEST_SPECIMEN2'
    assert obj5['attributes']['requested_taxonomy_id'] == 5678
    assert obj5['attributes']['status'] == 'Pending'
    assert obj5['relationships']['user']['data']['id'] == '200'


def test_request_creator(client, api_path):
    body = [
        {
            'species_id': 1234,
            'specimen_id': 'SPECIMEN1'  # New
        },
        {
            'species_id': 1234,
            'specimen_id': 'SPECIMEN2',  # New, with requested_taxonomy_id
            'requested_taxonomy_id': 5678
        },
        {
            'species_id': 1235,
            'specimen_id': 'SPECIMEN3',  # Species doesn't exist
            'requested_taxonomy_id': 6789
        },
        {
            'species_id': 1234,
            'specimen_id': 'TEST_SPECIMEN1'  # ToLID already exists
        },
        {
            'species_id': 1235,
            'specimen_id': 'TEST_SPECIMEN2'  # Request already exists
        }
    ]
    response = client.post(api_path + '/request/create', json=body)
    assert response.status_code == 200

    obj1 = response.json['data'][0]
    assert obj1['id'] == 'abCdeFghi2'
    assert obj1['type'] == 'specimen'
    assert obj1['attributes']['number'] == 2
    assert obj1['attributes']['specimen_id'] == 'SPECIMEN1'
    assert obj1['attributes']['legacy_name'] == None
    assert obj1['relationships']['species']['data']['id'] == '1234'
    assert obj1['relationships']['user']['data']['id'] == '100'

    obj2 = response.json['data'][1]
    assert obj2['id'] == 'abCdeFghi3'
    assert obj2['type'] == 'specimen'
    assert obj2['attributes']['number'] == 3
    assert obj2['attributes']['specimen_id'] == 'SPECIMEN2'
    assert obj2['attributes']['legacy_name'] == None
    assert obj2['attributes']['requested_taxonomy_id'] == 5678
    assert obj2['relationships']['species']['data']['id'] == '1234'
    assert obj2['relationships']['user']['data']['id'] == '100'

    obj3 = response.json['data'][2]
    assert obj3['type'] == 'request'
    assert obj3['attributes']['species_id'] == 1235
    assert obj3['attributes']['specimen_id'] == 'SPECIMEN3'
    assert obj3['attributes']['requested_taxonomy_id'] == 6789
    assert obj3['attributes']['status'] == 'Pending'
    assert obj3['relationships']['user']['data']['id'] == '100'

    obj4 = response.json['data'][3]
    assert obj4['type'] == 'specimen'
    assert obj4['id'] == 'abCdeFghi1'
    assert obj4['attributes']['number'] == 1
    assert obj4['attributes']['specimen_id'] == 'TEST_SPECIMEN1'
    assert obj2['relationships']['species']['data']['id'] == '1234'
    assert obj4['relationships']['user']['data']['id'] == '200'

    obj5 = response.json['data'][4]
    assert obj5['type'] == 'request'
    assert obj5['attributes']['species_id'] == 1235
    assert obj5['attributes']['specimen_id'] == 'TEST_SPECIMEN2'
    assert obj5['attributes']['requested_taxonomy_id'] == 5678
    assert obj5['attributes']['status'] == 'Pending'
    assert obj5['relationships']['user']['data']['id'] == '200'
