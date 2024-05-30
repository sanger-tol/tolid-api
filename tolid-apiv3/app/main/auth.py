# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from typing import Optional

from tol.api_base2.auth import AuthInspector
from tol.api_base2.misc import CtxGetter, default_ctx_getter
from tol.core.datasource_filter import AndFilter
from tol.core.operator import OperatorMethod


def create_auth_inspector(
    admin_role: str = 'admin',
    ctx_getter: CtxGetter = default_ctx_getter
) -> AuthInspector:

    def __inspector(
        object_type: str,
        method: OperatorMethod
    ) -> Optional[AndFilter]:
        pass

    return __inspector
