"""Change password_hash to text type

Revision ID: be2d94810042
Revises: a63d9d1e1d50
Create Date: 2022-02-15 19:48:36.489908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be2d94810042'
down_revision = 'a63d9d1e1d50'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'secrets',
        column_name='password_hash',
        type=sa.Text,
        existing_type=sa.String(5000),
    )


def downgrade():
    op.alter_column(
        'secrets',
        column_name='password_hash',
        existing_type=sa.Text,
        type=sa.String(5000),
    )
