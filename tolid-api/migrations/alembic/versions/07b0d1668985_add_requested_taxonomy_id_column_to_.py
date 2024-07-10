"""add requested_taxonomy_id column to specimen

Revision ID: 07b0d1668985
Revises: a3908275181e
Create Date: 2024-07-03 09:50:29.424468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07b0d1668985'
down_revision = 'a3908275181e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('specimen', sa.Column('requested_taxonomy_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'specimen', ['specimen_id', 'species_id'])


def downgrade():
    op.drop_column('specimen', 'requested_taxonomy_id')
