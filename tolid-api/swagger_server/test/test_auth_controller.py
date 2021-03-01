from __future__ import absolute_import

from swagger_server.test import BaseTestCase
from swagger_server.model import db, TolidState
import urllib.parse
import os
import responses


class TestAuthController(BaseTestCase):

    def test_login(self):
        response = self.client.open(
            '/api/v2/auth/login',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Get the state
        state = db.session.query(TolidState).one_or_none()
        params = {"client_id": os.getenv('ELIXIR_CLIENT_ID'),
                  "response_type": "code",
                  "state": state.state,
                  "redirect_uri": os.getenv('ELIXIR_REDIRECT_URI'),
                  "scope": 'openid profile email'}
        expect = {"loginUrl": "https://login.elixir-czech.org/oidc/authorize?"
                  + urllib.parse.urlencode(params)}
        self.assertEquals(expect, response.json)


    # The real version of this does a call to the Elixir service. We mock that call here
    @responses.activate
    def test_token(self):
        mock_response_from_elixir = {"access_token": "9876",
                                     "expires_in": 3599,
                                     "id_token": "5432",
                                     "scope": "openid email profile",
                                     "token_type": "Bearer"}
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
        mock_response_from_elixir = {"name": "Elixir User",
                                     "email": "elixir-user@sanger.ac.uk",
                                     "organisation": "Sanger Institute"}
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
                  'organisation': 'Sanger Institute',
                  'roles': []}
        self.assertEquals(expect, response.json)

    # The real version of this does a call to the Elixir service. We mock that call here
    @responses.activate
    def test_profile_existing_user(self):
        mock_response_from_elixir = {'email': 'test_user_creator@sanger.ac.uk',
                                     'name': 'test_user_creator',
                                     'organisation': 'Sanger Institute'}
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
                  'roles': [{"role": "creator"}]}
        self.assertEquals(expect, response.json)


if __name__ == '__main__':
    import unittest
    unittest.main()
