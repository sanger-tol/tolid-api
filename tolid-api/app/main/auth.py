# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from tol.api_base.auth import AuthInspector
from tol.api_base.auth.error import ForbiddenError
from tol.api_base.misc import (
    CtxGetter,
    default_ctx_getter
)
from tol.core.operator import OperatorMethod


def create_auth_inspector(
    ctx_getter: CtxGetter = default_ctx_getter,
    admin_role: str = 'admin'
) -> AuthInspector:

    WRITE_METHODS = (  # noqa N806
        OperatorMethod.DELETE,
        OperatorMethod.INSERT,
        OperatorMethod.UPDATE,
        OperatorMethod.UPSERT
    )

    def auth_inspector(
        object_type: str,
        method: OperatorMethod,
        *args,
        **kwargs
    ) -> None:

        # No access to user
        if object_type == 'user':
            raise ForbiddenError()

        # Only detail get for species and taxon
        if method == OperatorMethod.DETAIL and object_type not in ['species', 'taxon'] \
                and (ctx_getter().roles is None or admin_role not in ctx_getter().roles):
            raise ForbiddenError()

        # No access to writing if not authenticated
        if not ctx_getter().authenticated and method in WRITE_METHODS:
            raise ForbiddenError()

        # No access to specimen if not authenticated
        if object_type in ['specimen', 'request']:
            if not ctx_getter().authenticated:
                raise ForbiddenError()
            if method not in [OperatorMethod.PAGE, OperatorMethod.CURSOR]:
                raise ForbiddenError()
            # Add filter to only see own
            if ctx_getter().roles is None or admin_role not in ctx_getter().roles:
                return {
                    'user.id': {
                        'eq': {
                            'value': ctx_getter().user_id
                        }
                    }
                }

    return auth_inspector
