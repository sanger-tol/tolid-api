"""add id column to secondary_prefix

Revision ID: e5d7c78e45a4
Revises: 0a882096ad6d
Create Date: 2024-04-24 13:46:47.508725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5d7c78e45a4'
down_revision = '8c2eadd05c65'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE secondary_prefix DROP CONSTRAINT secondary_prefix_pkey;')
    op.execute('ALTER TABLE secondary_prefix ADD COLUMN id SERIAL PRIMARY KEY;')
    op.execute('ALTER TABLE secondary_prefix ADD UNIQUE (primary_prefix_letter, letter);')


def downgrade():
    pass
