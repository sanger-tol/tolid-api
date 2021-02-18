from __future__ import absolute_import

from swagger_server.test import BaseTestCase
from swagger_server.model import db, TolidState
import urllib.parse
import os


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


if __name__ == '__main__':
    import unittest
    unittest.main()
