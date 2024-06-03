# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from unittest.mock import Mock, create_autospec

import pytest

from tol.api_base2.auth import AuthInspector
from tol.api_base2.auth.error import ForbiddenError
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

    def test_basic_page_get(
        self,
        auth_context: AuthContext,
        ctx_getter: CtxGetter
    ):
        """
        a user with a `basic` role:

        - can page-get ToLID's
        - but additional filters added
          by `user.id`
        - can't do any other operation
        """

        auth_context.authenticated = True
        auth_context.user_id = '200'
        auth_context.roles = ['BASIC']

        inspector = create_auth_inspector(
            ctx_getter=ctx_getter
        )

        and_term = inspector(
            'specimen',
            OperatorMethod.PAGE
        )
        assert and_term == {
            'user.id': {
                'eq': {
                    'value': '200'
                }
            }
        }

        disallowed_methods = set(
            OperatorMethod
        ) - {OperatorMethod.PAGE}

        for op in disallowed_methods:
            with pytest.raises(ForbiddenError):
                inspector(
                    'specimen',
                    op
                )

    def test_no_roles_none_specimen(
        self,
        auth_context: AuthContext,
        ctx_getter: CtxGetter
    ):
        """
        a user with no roles can not perform
        any operation -> raise 403 always
        """

        auth_context.authenticated = True
        auth_context.user_id = '200'
        auth_context.roles = []

        inspector = create_auth_inspector(
            ctx_getter=ctx_getter
        )

        for op in OperatorMethod:
            with pytest.raises(ForbiddenError):
                inspector(
                    'specimen',
                    op
                )

    def test_no_detail_get(
        self,
        auth_context: AuthContext,
        ctx_getter: CtxGetter
    ):
        """
        No non-admin user can use
        `OperatorMethod.DETAIL`.
        """

        inspector = create_auth_inspector(
            ctx_getter=ctx_getter
        )

        auth_context.authenticated = False

        self.__assert_no_detail_get(inspector)

        auth_context.authenticated = True
        auth_context.user_id = '200'
        auth_context.roles = []

        self.__assert_no_detail_get(inspector)

    def __assert_no_detail_get(
        self,
        inspector: AuthInspector
    ) -> None:

        __TEST_TYPES = (
            'species',
            'specimen',
            'request'
        )

        for t in __TEST_TYPES:
            with pytest.raises(ForbiddenError):
                inspector(t, OperatorMethod.DETAIL)
