"""add unique prefix number on tolid

Revision ID: 7df274109286
Revises: 4728fef96e53
Create Date: 2024-08-05 08:23:51.037824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7df274109286'
down_revision = '4728fef96e53'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'specimen',
        ['species_id', 'number'],
        unique=True
    )


def downgrade():
    pass
