# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from connexion.exceptions import OAuthProblem

from main.model import TolidToken, db


def apikey_auth(token, required_scopes):
    # Direct from api-key (i.e. not Elixir)
    token_row = db.session.query(TolidToken) \
        .filter(TolidToken.token == token) \
        .one_or_none()

    if token_row is None:
        raise OAuthProblem('Invalid api-key and Elixir token')

    user = token_row.user
    return {'user': user.name, 'uid': user.id}
