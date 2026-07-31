# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import Optional

from tol.api_base.auth import CompositeAuthInspector
from tol.api_base.auth.error import ForbiddenError
from tol.api_base.misc import AuthContext, CtxGetter, default_ctx_getter
from tol.core.operator import OperatorMethod


def create_auth_inspector(
    admin_role: str = 'admin', ctx_getter: CtxGetter = default_ctx_getter
) -> CompositeAuthInspector:

    composite = CompositeAuthInspector(admin_role=admin_role, ctx_getter=ctx_getter)

    composite.forbid_noauth(['user', 'specimen', 'request'])

    @composite.auth(
        object_type='user',
    )
    def __user_auth(
        __object_type: str,
        op: OperatorMethod,
        auth_ctx: Optional[AuthContext] = None,
        bound_args: Optional[object] = None,
        **kwargs,
    ):
        return {'id': {'eq': {'value': auth_ctx.user_id}}}

    @composite.auth(
        object_type='specimen',
    )
    def __specimen_auth(
        __object_type: str,
        op: OperatorMethod,
        auth_ctx: Optional[AuthContext] = None,
        bound_args: Optional[object] = None,
        **kwargs,
    ):
        if op not in [OperatorMethod.PAGE, OperatorMethod.CURSOR]:
            raise ForbiddenError()
        return {'user.id': {'eq': {'value': auth_ctx.user_id}}}

    @composite.auth(
        object_type='request',
    )
    def __request_auth(
        __object_type: str,
        op: OperatorMethod,
        auth_ctx: Optional[AuthContext] = None,
        bound_args: Optional[object] = None,
        **kwargs,
    ):
        if op not in [OperatorMethod.PAGE, OperatorMethod.CURSOR]:
            raise ForbiddenError()
        return {'user.id': {'eq': {'value': auth_ctx.user_id}}}

    @composite.noauth
    def __no_write_without_auth(__object_type: str, op: OperatorMethod, **kwargs):

        __WRITE_METHODS = (  # noqa N806
            OperatorMethod.DELETE,
            OperatorMethod.INSERT,
            OperatorMethod.UPDATE,
            OperatorMethod.UPSERT,
        )

        if op in __WRITE_METHODS:
            raise ForbiddenError()

    @composite.always
    def __no_detail_get(__object_type: str, op: OperatorMethod, **kwargs):
        if op == OperatorMethod.DETAIL and __object_type not in ['species', 'taxon']:
            raise ForbiddenError()

    return composite
