"""update user table

Revision ID: 10e1d2c2e7b2
Revises: 7df274109286
Create Date: 2026-07-29 19:36:12.225055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10e1d2c2e7b2'
down_revision = '7df274109286'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'user',
        'organisation',
        new_column_name='workplace'
    )


def downgrade():
    op.alter_column(
        'user',
        'workplace',
        new_column_name='organisation'
    )
