# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import Optional

import connexion

from flask import jsonify

from main.model import TolidUser, db


class ForbiddenError(Exception):
    # TODO - work out connexion error handling - and `raise` this properly

    @property
    def response(self):
        return jsonify(
            {'detail': 'User does not have permission to use this function'}
        ), 403


def check_role(role_names: list[str]) -> Optional[ForbiddenError]:
    user = db.session.query(TolidUser) \
        .filter(TolidUser.id == connexion.context['user']) \
        .one_or_none()

    user_role_names = user.role_names

    for name in role_names:
        if name in user_role_names:
            return

    return ForbiddenError()


def check_admin() -> Optional[ForbiddenError]:
    return check_role(['admin'])


def check_creator() -> Optional[ForbiddenError]:
    return check_role(['admin', 'creator'])
