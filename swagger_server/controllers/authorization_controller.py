from typing import List
import connexion
import json
import os
from connexion.exceptions import OAuthProblem
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

def get_api_keys(api_token=None):
    token_owner = None 
    try:
        with open(os.path.join('instance', 'config.json')) as config_file:
            tokens = json.load(config_file)
        token_owner = tokens[api_token]
        if token_owner:
            print("AUTHENTICATION INFO: Found valid api-token for user " + token_owner["user"])
        else:
            print("AUTHENTICATION ERROR: Could not find a user for token " + api_token)
    except Exception as e:
        print(str(e))

    return token_owner


def apikey_auth(token, required_scopes):

    # info = TOKEN_DB.get(token, None)
    token_found = get_api_keys(api_token=token)

    if not token_found:
        raise OAuthProblem('Invalid api-key token')

    return token_found