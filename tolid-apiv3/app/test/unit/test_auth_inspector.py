# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock, create_autospec

import pytest

from tol.api_base2.misc import (
    AuthContext,
    CtxGetter
)
from tol.core.operator import OperatorMethod

from main.auth import create_auth_inspector


@pytest.fixture(scope='function')
def auth_context() -> AuthContext:
    return create_autospec(
        AuthContext,
        spec_set=True
    )


@pytest.fixture(scope='function')
def ctx_getter(
    auth_context: AuthContext
) -> CtxGetter:

    mock_ctx_getter = Mock(spec_set=True)
    mock_ctx_getter.return_value = auth_context

    return mock_ctx_getter


class TestAuthInspector:
    """
    `create_auth_inspector()` behaves for various cases
    """

    def test_admin_all(
        self,
        auth_context: AuthContext,
        ctx_getter: CtxGetter
    ):
        """
        a user with the `admin` role:

        - can perform any operation
        - has no additional filter terms
        """

        auth_context.user_id = '100'
        auth_context.roles = [
            'le_admin',
            'something_else__unimportant'
        ]

        inspector = create_auth_inspector(
            admin_role='le_admin',
            ctx_getter=ctx_getter
        )

        for op in OperatorMethod:
            and_term = inspector(
                'nonsense_type',
                op
            )
            assert not and_term

    def test_basic_page_get(self):
        """
        a user with a `basic` role:

        - can page-get ToLID's
        - but additional filters added
          by `user.id`
        - can't do any other operation
        """

    def test_no_roles_none(self):
        """
        a user with no roles can not perform
        any operation -> raise 403 always
        """
