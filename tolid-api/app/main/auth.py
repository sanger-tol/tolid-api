# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import Optional

from tol.api_base.auth import CompositeAuthInspector
from tol.api_base.auth.error import ForbiddenError
from tol.api_base.misc import (
    AuthContext,
    CtxGetter,
    default_ctx_getter
)
from tol.core.operator import OperatorMethod


def create_auth_inspector(
    admin_role: str = 'admin',
    ctx_getter: CtxGetter = default_ctx_getter
) -> CompositeAuthInspector:

    composite = CompositeAuthInspector(
        admin_role=admin_role,
        ctx_getter=ctx_getter
    )

    composite.forbid('user')

    composite.forbid_noauth(['specimen', 'request'])

    @composite.noauth
    def __no_write_without_auth(
        __object_type: str,
        op: OperatorMethod,
        **kwargs
    ):

        __WRITE_METHODS = (  # noqa N806
            OperatorMethod.DELETE,
            OperatorMethod.INSERT,
            OperatorMethod.UPDATE,
            OperatorMethod.UPSERT,
        )

        if op in __WRITE_METHODS:
            raise ForbiddenError()

    @composite.always
    def __no_detail_get(
        object_type: str,
        op: OperatorMethod,
        **kwargs
    ):

        if object_type in ['species', 'taxon']:
            return

        if op == OperatorMethod.DETAIL:
            raise ForbiddenError()

    @composite.auth(
        object_type=['specimen', 'request'],
    )
    def __specimen_request_auth(
        __object_type: str,
        op: OperatorMethod,
        auth_context: Optional[AuthContext] = None
    ):

        __ALLOWED_METHODS = (  # noqa N806
            OperatorMethod.PAGE,
        )

        if auth_context is None or auth_context.roles is None:
            raise ForbiddenError()

        if op not in __ALLOWED_METHODS:
            raise ForbiddenError()

        return {
            'user.id': {
                'eq': {
                    'value': auth_context.user_id
                }
            }
        }

    return composite
