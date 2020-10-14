from typing import List
import connexion
from connexion.exceptions import OAuthProblem
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

TOKEN_DB = {
    '1234': {
        'uid': 100
    }
}

def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem('Invalid api-key token')

    return info