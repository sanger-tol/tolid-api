"""unique prefix on species

Revision ID: 4728fef96e53
Revises: 07b0d1668985
Create Date: 2024-07-15 07:04:42.514148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4728fef96e53'
down_revision = '07b0d1668985'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'species',
        'prefix',
        unique=True
    )


def downgrade():
    pass
