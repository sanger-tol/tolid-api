# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from functools import wraps
from typing import Any, Callable

from tol.api_base2.auth import require_auth
from tol.api_base2.auth.error import ForbiddenError
from tol.api_base2.misc import default_ctx_getter


require_admin = require_auth(role='admin')


def require_creator(func: Callable) -> Any:

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        roles = default_ctx_getter().roles

        if 'admin' not in roles and 'creator' not in roles:
            raise ForbiddenError()

        return func(*args, **kwargs)

    return wrapper
