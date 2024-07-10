"""oidc_state

Revision ID: 8c2eadd05c65
Revises: 0a882096ad6d
Create Date: 2024-04-24 13:33:28.160511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c2eadd05c65'
down_revision = '0a882096ad6d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'oidc_state',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('created_at', sa.DateTime, nullable=False)
    )


def downgrade():
    pass
