"""Change password_hash length to undefined length

Revision ID: 9da155b08e70
Revises: dc680b0db750
Create Date: 2022-02-15 20:15:32.910631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9da155b08e70'
down_revision = 'dc680b0db750'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'secrets',
        sa.Column('encoded_secret', sa.UnicodeText, nullable=True)
    )
    op.drop_column('secrets', 'password_hash')


def downgrade():
    op.add_column(
        'secrets',
        sa.Column('password_hash', sa.Text, nullable=True)
    )
    op.drop_column('secrets', 'password_hash')
