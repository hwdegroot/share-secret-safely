"""Add ttl to secrets

Revision ID: dc680b0db750
Revises: be2d94810042
Create Date: 2022-02-15 20:06:26.759358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc680b0db750'
down_revision = 'be2d94810042'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'secrets',
        sa.Column('ttl', sa.Integer, nullable=True, default=None)
    )


def downgrade():
    op.add_column(
        'secrets',
        'ttl'
    )
