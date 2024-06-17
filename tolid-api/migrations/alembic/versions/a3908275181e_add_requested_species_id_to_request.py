"""add requested_species_id to request

Revision ID: a3908275181e
Revises: e5d7c78e45a4
Create Date: 2024-06-10 10:39:13.339561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3908275181e'
down_revision = 'e5d7c78e45a4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('request', sa.Column('requested_taxonomy_id', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('request', 'requested_taxonomy_id')
