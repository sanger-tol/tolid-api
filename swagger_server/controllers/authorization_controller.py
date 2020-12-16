from connexion.exceptions import OAuthProblem
from swagger_server.model import db, TolidUser

def apikey_auth(token, required_scopes):

    # info = TOKEN_DB.get(token, None)
    user = db.session.query(TolidUser).filter(TolidUser.api_key == token).one_or_none()

    if user is None:
        raise OAuthProblem('Invalid api-key token')

    return { "user": user.name, "uid": user.user_id}