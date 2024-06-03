# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import Optional

from tol.api_base2.auth import CompositeAuthInspector
from tol.api_base2.auth.error import ForbiddenError
from tol.api_base2.misc import (
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

    @composite.handle_noauth
    def __no_write_without_auth(
        __object_type: str,
        op: OperatorMethod,
        **kwargs
    ):

        __WRITE_METHODS = (  # noqa N806
            OperatorMethod.DELETE,
            OperatorMethod.UPDATE,
            OperatorMethod.UPSERT,
        )

        if op in __WRITE_METHODS:
            raise ForbiddenError()

    @composite.handle_noauth
    @composite.handle
    def __no_forbidden_types(
        object_type: str,
        __op: OperatorMethod,
        **kwargs
    ):

        __FORBIDDEN_TYPES = (  # noqa N806
            'user',
        )

        if object_type in __FORBIDDEN_TYPES:
            raise ForbiddenError()

    @composite.handle
    @composite.handle_noauth
    def __no_detail_get(
        __object_type: str,
        op: OperatorMethod,
        **kwargs
    ):

        if op == OperatorMethod.DETAIL:
            raise ForbiddenError()

    @composite.handle_type('specimen')
    def __specimen(
        __object_type: str,
        op: OperatorMethod,
        auth_context: Optional[AuthContext] = None
    ):

        __ALLOWED_METHODS = (  # noqa N806
            OperatorMethod.PAGE,
        )

        if not auth_context.roles:
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
