# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from tol.api_base2.auth import CompositeAuthInspector
from tol.api_base2.auth.error import ForbiddenError
from tol.api_base2.misc import CtxGetter, default_ctx_getter
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
) -> CompositeAuthInspector:

    composite = CompositeAuthInspector(
        admin_role=admin_role,
        ctx_getter=ctx_getter
    )

    return composite
