# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import Optional

from tol.api_base2.auth import AuthInspector
from tol.api_base2.auth.error import ForbiddenError
from tol.api_base2.misc import CtxGetter, default_ctx_getter
from tol.core.datasource_filter import AndFilter
from tol.core.operator import OperatorMethod


__WRITE_METHODS = [
    OperatorMethod.DELETE,
    OperatorMethod.UPDATE,
    OperatorMethod.UPSERT,
]


__FORBIDDEN_TYPES = [
    'user',
]


def create_auth_inspector(
    admin_role: str = 'admin',
    ctx_getter: CtxGetter = default_ctx_getter
) -> AuthInspector:

    def __inspector(
        object_type: str,
        method: OperatorMethod
    ) -> Optional[AndFilter]:

        auth_ctx = ctx_getter()
        roles = auth_ctx.roles

        if admin_role in roles:
            return

        if object_type in __FORBIDDEN_TYPES:
            raise ForbiddenError()

        if not roles:
            if method in __WRITE_METHODS:
                raise ForbiddenError()
            if object_type == 'specimen':
                raise ForbiddenError()
            return

        if method == OperatorMethod.DETAIL:
            raise ForbiddenError()

        if object_type == 'specimen':
            if method == OperatorMethod.PAGE:
                return {
                    'user.id': {
                        'eq': {
                            'value': auth_ctx.user_id
                        }
                    }
                }
            else:
                raise ForbiddenError()

    return __inspector
