from swagger_server.model import db, TolidUser, TolidState
from flask import jsonify
import uuid
import urllib.parse
from datetime import datetime, timedelta
import os
import requests
from requests.auth import HTTPBasicAuth

from connexion.exceptions import OAuthProblem


def apikey_auth(token, required_scopes):
    # info = TOKEN_DB.get(token, None)
    user = db.session.query(TolidUser) \
        .filter(TolidUser.api_key == token) \
        .one_or_none()

    if user is None:
        raise OAuthProblem('Invalid api-key token')

    return {"user": user.name, "uid": user.user_id}


def login():
    state_uuid = str(uuid.uuid4())
    params = {"client_id": os.getenv('ELIXIR_CLIENT_ID'),
              "response_type": "code",
              "state": state_uuid,
              "redirect_uri": os.getenv('ELIXIR_REDIRECT_URI'),
              "scope": 'openid profile email'}
    # Save the state in a table so that we can use it
    state = TolidState()
    state.state = state_uuid
    db.session.add(state)
    db.session.commit()

    # Clear out states older than one hour so this table doesn't fill up
    since = datetime.now() - timedelta(hours=1)
    db.session.query(TolidState) \
        .filter(TolidState.created_at < since) \
        .delete()
    db.session.commit()

    return jsonify({'loginUrl': "https://login.elixir-czech.org/oidc/authorize?"
                   + urllib.parse.urlencode(params)})

def get_token_from_callback(body=None):
    # Check that we know about this state
    state_from_db = db.session.query(TolidState) \
        .filter(TolidState.state == body['state']) \
        .one_or_none()
    if state_from_db is None:
        return jsonify({'detail': 'Unknown state'}), 404
    client_auth = HTTPBasicAuth(os.getenv('ELIXIR_CLIENT_ID'), os.getenv('ELIXIR_CLIENT_SECRET'))
    post_data = {"grant_type": "authorization_code",
                 "code": body['code'],
                 "redirect_uri": os.getenv('ELIXIR_REDIRECT_URI')}
    response = requests.post('https://login.elixir-czech.org/oidc/token',
                             auth=client_auth,
                             data=post_data)
    return jsonify(response.json())

def create_user_profile(body=None):
    # Get the user infromation from Elixir for this token
    response = requests.get('https://login.elixir-czech.org/oidc/userinfo',
                            headers={"Authorization": "Bearer " + body["token"]})
    user_info_from_elixir = response.json()
    if user_info_from_elixir.get('error') is None:
        user = db.session.query(TolidUser) \
        .filter(TolidUser.email == user_info_from_elixir['email']) \
        .one_or_none()
        if not user:
            # A new user for the system - create entry
            user = TolidUser()
            user.email = user_info_from_elixir['email']
            user.name = user_info_from_elixir['name']
            user.organisation = user_info_from_elixir['organisation']
            db.session.add(user)
        # Save the token so that we can authenticate against it in future
        user.token = body["token"]
        db.session.commit()
        return jsonify(user)
    else:
        return jsonify({'detail': 'Error getting data from Elixir'}), 404