# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from __future__ import absolute_import

import json
import os
import urllib.parse
from datetime import datetime, timedelta, timezone
from test.system import BaseTestCase

from connexion.exceptions import OAuthProblem

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from jwt import (
    JWT
)
from jwt.jwk import RSAJWK
from jwt.utils import get_int_from_datetime

from main.controllers.auth_controller import apikey_auth
from main.model import TolidState, db

import responses


class TestAuthController(BaseTestCase):

    def test_api_key_auth(self):
        # Nothing
        try:
            apikey_auth('MadeUpKey', None)
            self.assertEqual(True, False)
        except OAuthProblem:
            pass

        # Auth using API key
        ret = apikey_auth(self.user3.api_key, None)
        expect = {'user': self.user3.name, 'uid': self.user3.user_id}
        self.assertEqual(expect, ret)

        # Mock Elixir key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        key = RSAJWK(private_key)
        os.environ['ELIXIR_JWK'] = json.dumps(key.to_dict())
        instance = JWT()

        # Expired Elixir token
        message = {
            'iss': 'https://example.com/',
            'sub': '123456',
            'iat': get_int_from_datetime(datetime.now(timezone.utc) - timedelta(hours=2)),
            'exp': get_int_from_datetime(datetime.now(timezone.utc) - timedelta(hours=1)),
        }
        jwt = instance.encode(message, key, alg='RS256')
        self.user3.token = jwt
        db.session.commit()
        try:
            apikey_auth(self.user3.token, None)
            self.assertEqual(True, False)
        except OAuthProblem:
            pass

        # Faked Elixir token
        private_key2 = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        key2 = RSAJWK(private_key2)
        message = {
            'iss': 'https://example.com/',
            'sub': '123456',
            'iat': get_int_from_datetime(datetime.now(timezone.utc)),
            'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(hours=1)),
        }
        jwt = instance.encode(message, key2, alg='RS256')
        self.user3.token = jwt
        db.session.commit()
        try:
            apikey_auth(self.user3.token, None)
            self.assertEqual(True, False)
        except OAuthProblem:
            pass

        # Correct Elixir Token
        jwt = instance.encode(message, key, alg='RS256')
        self.user3.token = jwt
        db.session.commit()
        ret = apikey_auth(self.user3.token, None)
        expect = {'user': self.user3.name, 'uid': self.user3.user_id}
        self.assertEqual(expect, ret)

    def test_login(self):
        response = self.client.open(
            '/api/v2/auth/login',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Get the state
        state = db.session.query(TolidState).one_or_none()
        params = {'client_id': os.getenv('ELIXIR_CLIENT_ID'),
                  'response_type': 'code',
                  'state': state.state,
                  'redirect_uri': os.getenv('ELIXIR_REDIRECT_URI'),
                  'scope': 'openid profile email'}
        expect = {'loginUrl': 'https://login.elixir-czech.org/oidc/authorize?'
                  + urllib.parse.urlencode(params)}
        self.assertEqual(expect, response.json)

    # The real version of this does a call to the Elixir service. We mock that call here
    @responses.activate
    def test_token(self):
        mock_response_from_elixir = {'access_token': '9876',
                                     'expires_in': 3599,
                                     'id_token': '5432',
                                     'scope': 'openid email profile',
                                     'token_type': 'Bearer'}
        responses.add(responses.POST, 'https://login.elixir-czech.org/oidc/token',
                      json=mock_response_from_elixir, status=200)

        # Set up the state
        state = TolidState()
        state.state = '1234'
        db.session.add(state)
        db.session.commit()

        # Do the actual request
        response = self.client.open(
            '/api/v2/auth/token',
            method='POST',
            json={'state': '1234', 'code': '5678'})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Our API passes the Elixir response straight on
        self.assertEqual(response.json, mock_response_from_elixir)

    # The real version of this does a call to the Elixir service. We mock that call here
    @responses.activate
    def test_profile_new_user(self):
        mock_response_from_elixir = {'name': 'Elixir User',
                                     'email': 'elixir-user@sanger.ac.uk',
                                     'organisation': 'Sanger Institute'}
        responses.add(responses.GET, 'https://login.elixir-czech.org/oidc/userinfo',
                      json=mock_response_from_elixir, status=200)

        response = self.client.open(
            '/api/v2/auth/profile',
            method='POST',
            json={'token': '1234'})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        expect = {'email': 'elixir-user@sanger.ac.uk',
                  'name': 'Elixir User',
                  'organisation': '',
                  'roles': []}
        self.assertEqual(expect, response.json)

    # The real version of this does a call to the Elixir service. We mock that call here
    @responses.activate
    def test_profile_existing_user(self):
        mock_response_from_elixir = {'email': 'test_user_creator@sanger.ac.uk',
                                     'name': 'test_user_creator'}
        responses.add(responses.GET, 'https://login.elixir-czech.org/oidc/userinfo',
                      json=mock_response_from_elixir, status=200)

        response = self.client.open(
            '/api/v2/auth/profile',
            method='POST',
            json={'token': '1234'})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        expect = {'email': 'test_user_creator@sanger.ac.uk',
                  'name': 'test_user_creator',
                  'organisation': 'Sanger Institute',
                  'roles': [{'role': 'creator'}]}
        self.assertEqual(expect, response.json)

    # The real version of this does a call to the Elixir service. We mock that call here
    @responses.activate
    def test_logout(self):
        mock_response_from_elixir = {}
        responses.add(responses.GET, 'https://login.elixir-czech.org/oidc/revoke',
                      json=mock_response_from_elixir, status=200)

        # Do the actual request
        response = self.client.open(
            '/api/v2/auth/logout',
            method='DELETE',
            query_string={'token': '1234'})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Our API passes the Elixir response straight on
        self.assertEqual(response.json, mock_response_from_elixir)


if __name__ == '__main__':
    import unittest
    unittest.main()
