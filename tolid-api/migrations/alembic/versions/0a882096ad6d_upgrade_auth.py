"""upgrade auth

Revision ID: 0a882096ad6d
Revises: a6d81470da70
Create Date: 2024-04-10 07:18:08.700170

"""

from datetime import datetime, timedelta
from functools import reduce
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm


# revision identifiers, used by Alembic.
revision = '0a882096ad6d'
down_revision = 'a6d81470da70'
branch_labels = None
depends_on = None


def upgrade():
    # rename `user`.[user_id -> id]
    op.alter_column('user', 'user_id', new_column_name='id')



    # get data to move
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    user_roles_raw = session.execute(
        sa.text(
            '''
            SELECT user_id, role
            FROM role
            '''
        )
    ).fetchall()
    user_roles = (
        (user_id, role_name)
        for user_id, role_name
        in user_roles_raw
    )

    def __add(d: dict[str, list[int]], pair: tuple[int, str]) -> dict[str, list[int]]:
        user_id, role_name = pair
        old = d.get(role_name, [])
        d[role_name] = old + [user_id]
        return d

    role_bindings = reduce(
        lambda d, p: __add(d, p),
        user_roles,
        {}
    )

    user_tokens_raw = session.execute(
        sa.text(
            '''
            SELECT id, token, api_key
            FROM "user"
            '''
        )
    ).fetchall()

    user_tokens = {
        u: t
        for (u, t, _) in user_tokens_raw
        if t is not None
    }

    user_api_keys = {
        u: a
        for (u, _, a) in user_tokens_raw
        if a is not None
    }



    # drop redundant columns from `user`
    op.drop_column('user', 'token')
    op.drop_column('user', 'api_key')



    # completely remove `role` and create anew
    op.drop_table('role')

    op.create_table(
        'role',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False, unique=True)
    )



    # add new tables
    op.create_table(
        'token',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('token', sa.String(), unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('oidc', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'])
    )

    op.create_table(
        'role_binding',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'])
    )



    # insert the `role` data
    role_ids = {
        name: i
        for i, name in enumerate(role_bindings, start=1)
    }

    for role_name, i in role_ids.items():
        session.execute(
            sa.text(
                f'''
                INSERT INTO role(id, name)
                VALUES ({i}, '{role_name}')
                '''
            )
        )



    # insert the `role_binding` data
    for role_name, user_ids in role_bindings.items():
        role_id = role_ids[role_name]
        for user_id in user_ids:
            session.execute(
                sa.text(
                    f'''
                    INSERT INTO role_binding(user_id, role_id)
                    VALUES ({user_id}, {role_id})
                    '''
                )
            )



    # insert the OIDC `token` data
    oidc_expiry_date = datetime.now() + timedelta(days=7)

    for user_id, oidc_token in user_tokens.items():
        session.execute(
            sa.text(
                f'''
                INSERT into token(token, expires_at, oidc, user_id)
                VALUES (
                    '{oidc_token}',
                    TIMESTAMP '{oidc_expiry_date.strftime("%Y-%m-%d %H:%M:%S")}',
                    true,
                    {user_id}
                )
                '''
            )
        )



    # insert the api_key `token` data
    api_key_expiry_date = datetime.now() + timedelta(days=3650)

    for user_id, api_key in user_api_keys.items():
        session.execute(
            sa.text(
                f'''
                INSERT into token(token, expires_at, oidc, user_id)
                VALUES (
                    '{api_key}',
                    TIMESTAMP '{api_key_expiry_date.strftime("%Y-%m-%d %H:%M:%S")}',
                    false,
                    {user_id}
                )
                '''
            )
        )


def downgrade():
    pass
