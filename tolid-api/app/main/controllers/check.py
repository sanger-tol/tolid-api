# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

import connexion

from flask import jsonify

from main.model import TolidUser, db


class ForbiddenError(Exception):

    @property
    def response(self):
        return jsonify(
            {'detail': 'User does not have permission to use this function'}
        ), 403



def check_role(role_names: list[str]) -> None:
    user = db.session.query(TolidUser) \
        .filter(TolidUser.user_id == connexion.context['user']) \
        .one_or_none()

    user_role_names = user.role_names

    for name in role_names:
        if name in user_role_names:
            return

    raise ForbiddenError()


def check_admin() -> None:
    check_role(['admin'])


def check_creator() -> None:
    check_role(['admin', 'creator'])
