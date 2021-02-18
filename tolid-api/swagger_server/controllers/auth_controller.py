from swagger_server.model import db, TolidUser, TolidState
from flask import jsonify
import uuid
import urllib.parse
from datetime import datetime, timedelta
import os

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
